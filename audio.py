import logging
from typing import Optional

import numpy as np
import sounddevice as sd

logger = logging.getLogger(__name__)

SAMPLE_RATE = 16000
CHANNELS = 1
DTYPE = "float32"


class AudioRecorder:
    duration: float

    def __init__(self) -> None:
        self.duration = 0.0
        self._frames: list[np.ndarray] = []
        self._stream: Optional[sd.InputStream] = None

    def start(self) -> None:
        if self._stream is not None:
            self._stream.close()
            self._stream = None

        self._frames = []

        def _callback(
            indata: np.ndarray,
            frames: int,
            time: object,
            status: sd.CallbackFlags,
        ) -> None:
            self._frames.append(indata.copy())

        self._stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype=DTYPE,
            callback=_callback,
        )
        self._stream.start()
        logger.info("Recording started")

    def stop(self) -> np.ndarray:
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
        return audio
