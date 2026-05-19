import logging
from collections.abc import Callable
from typing import Optional

import numpy as np
import sounddevice as sd

logger = logging.getLogger(__name__)

SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = "float32"
CHUNK_INTERVAL: float = 5.0  # seconds between emitted chunks
CHUNK_OVERLAP: float = 0.3   # seconds of overlap with previous chunk boundary

_MIN_CHUNK_FRAMES = int(0.5 * SAMPLE_RATE)


class AudioRecorder:
    duration: float

    def __init__(self) -> None:
        self.duration = 0.0
        self._frames: list[np.ndarray] = []
        self._stream: Optional[sd.InputStream] = None
        self._total_frames: int = 0
        self._emitted_up_to: int = 0
        self._on_chunk: Callable[[np.ndarray], None] | None = None

    def start(self, on_chunk: Callable[[np.ndarray], None] | None = None) -> None:
        """Start recording. on_chunk called every CHUNK_INTERVAL seconds."""
        if self._stream is not None:
            self._stream.close()
            self._stream = None

        self._frames = []
        self._total_frames = 0
        self._emitted_up_to = 0
        self._on_chunk = on_chunk

        chunk_frames = int(CHUNK_INTERVAL * SAMPLE_RATE)
        overlap_frames = int(CHUNK_OVERLAP * SAMPLE_RATE)

        def _callback(
            indata: np.ndarray,
            frames: int,
            time: object,
            status: sd.CallbackFlags,
        ) -> None:
            self._frames.append(indata.copy())
            self._total_frames += frames

            if self._on_chunk is None:
                return

            if self._total_frames - self._emitted_up_to < chunk_frames:
                return

            start = max(0, self._emitted_up_to - overlap_frames)
            audio = np.concatenate(self._frames, axis=0).reshape(-1)
            chunk = audio[start : self._total_frames]
            self._emitted_up_to = self._total_frames

            if len(chunk) >= _MIN_CHUNK_FRAMES:
                self._on_chunk(chunk)
            else:
                logger.debug("Chunk too short (%d frames), discarded", len(chunk))

        self._stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype=DTYPE,
            callback=_callback,
        )
        self._stream.start()
        logger.info("Recording started")

    def stop(self) -> np.ndarray:
        """Stop recording. Returns residual audio after the last emitted chunk."""
        if self._stream is not None:
            self._stream.stop()
            self._stream.close()
            self._stream = None

        if self._frames:
            audio = np.concatenate(self._frames, axis=0).reshape(-1)
        else:
            audio = np.zeros(0, dtype=DTYPE)

        self.duration = len(audio) / SAMPLE_RATE
        logger.info("Recording stopped — %.2fs captured", self.duration)

        if self._on_chunk is not None:
            return audio[self._emitted_up_to :]
        return audio
