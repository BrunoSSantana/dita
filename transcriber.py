import logging

import numpy as np
from faster_whisper import WhisperModel

logger = logging.getLogger(__name__)


class Transcriber:
    language: str

    def __init__(
        self,
        model: str,
        device: str,
        compute_type: str,
        language: str,
    ) -> None:
        self.language = language
        logger.info(
            "Loading Whisper model '%s' on %s (%s)...", model, device, compute_type
        )
        self._model = WhisperModel(model, device=device, compute_type=compute_type)
        logger.info("Whisper model loaded.")

    def transcribe(self, audio: np.ndarray, sample_rate: int = 16000) -> str:
        if audio is None or audio.size == 0:
            return ""

        try:
            segments, _ = self._model.transcribe(
                audio,
                language=self.language or None,
                beam_size=5,
                vad_filter=True,
                vad_parameters={"min_silence_duration_ms": 500},
            )
            return "".join(segment.text for segment in segments).strip()
        except Exception:
            logger.exception("Transcription failed")
            return ""
