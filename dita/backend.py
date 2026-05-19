import logging
from concurrent.futures import Future, ThreadPoolExecutor

import numpy as np
import pyperclip

from dita.audio import SAMPLE_RATE, AudioRecorder
from dita.config import load_config
from dita.transcriber import Transcriber

logger = logging.getLogger(__name__)

_MIN_CHUNK_FRAMES = int(0.5 * SAMPLE_RATE)


class Backend:
    recording: bool

    def __init__(self) -> None:
        self.recording = False
        self.window = None
        cfg = load_config()
        self._recorder = AudioRecorder()
        self._transcriber = Transcriber(
            model=cfg["model"],
            device=cfg["device"],
            compute_type=cfg["compute_type"],
            language=cfg["language"],
        )
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._chunk_futures: list[Future] = []
        self._chunk_counter: int = 0

    def set_window(self, window) -> None:
        self.window = window

    def _submit_chunk(self, audio: np.ndarray, idx: int) -> Future:
        def _transcribe() -> tuple[int, str]:
            try:
                text = self._transcriber.transcribe(audio)
                logger.info("Chunk %d done: %d chars", idx, len(text))
                if self.window and text:
                    safe = text.replace("\\", "\\\\").replace("'", "\\'")
                    try:
                        self.window.evaluate_js(
                            f"window.onPartialTranscript"
                            f"&&window.onPartialTranscript('{safe}')"
                        )
                    except Exception:
                        logger.exception("evaluate_js partial transcript failed")
                return idx, text
            except Exception:
                logger.exception("Chunk %d transcription failed", idx)
                return idx, ""

        return self._executor.submit(_transcribe)

    def start_recording(self) -> dict:
        try:
            self._chunk_futures = []
            self._chunk_counter = 0

            def on_chunk(audio: np.ndarray) -> None:
                idx = self._chunk_counter
                self._chunk_counter += 1
                future = self._submit_chunk(audio, idx)
                self._chunk_futures.append(future)

            self._recorder.start(on_chunk=on_chunk)
            self.recording = True
            return {"ok": True, "data": None}
        except Exception as e:
            logger.exception("start_recording failed")
            return {"ok": False, "error": str(e)}

    def stop_recording(self) -> dict:
        try:
            residual = self._recorder.stop()
            self.recording = False
            duration = self._recorder.duration

            # Block until all chunk transcriptions finish (thread safety: max_workers=1)
            chunk_texts: list[tuple[int, str]] = []
            for future in self._chunk_futures:
                try:
                    chunk_texts.append(future.result())
                except Exception:
                    logger.exception("Chunk future failed")

            chunk_texts.sort(key=lambda x: x[0])

            # Transcribe residual only after all chunk futures complete
            residual_text = ""
            if residual.size >= _MIN_CHUNK_FRAMES:
                residual_text = self._transcriber.transcribe(residual)

            parts = [t for _, t in chunk_texts] + (
                [residual_text] if residual_text else []
            )
            text = " ".join(p for p in parts if p).strip()

            cfg = load_config()
            if cfg.get("auto_copy") and text:
                pyperclip.copy(text)

            return {"ok": True, "data": {"text": text, "duration": duration}}
        except Exception as e:
            logger.exception("stop_recording failed")
            self.recording = False
            return {"ok": False, "error": str(e)}

    def get_config(self) -> dict:
        try:
            return {"ok": True, "data": load_config()}
        except Exception as e:
            logger.exception("get_config failed")
            return {"ok": False, "error": str(e)}

    def close(self) -> None:
        if self.window is not None:
            self.window.hide()
