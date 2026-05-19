import logging

import pyperclip

from dita.audio import AudioRecorder
from dita.config import load_config
from dita.transcriber import Transcriber

logger = logging.getLogger(__name__)


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

    def set_window(self, window) -> None:
        self.window = window

    def start_recording(self) -> dict:
        try:
            self._recorder.start()
            self.recording = True
            return {"ok": True, "data": None}
        except Exception as e:
            logger.exception("start_recording failed")
            return {"ok": False, "error": str(e)}

    def stop_recording(self) -> dict:
        try:
            audio = self._recorder.stop()
            self.recording = False
            duration = self._recorder.duration
            text = self._transcriber.transcribe(audio)
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
