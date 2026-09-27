from pathlib import Path
from faster_whisper import WhisperModel
from .models import Transcription


class WhisperTranscriber:
    def __init__(
        self,
        model: str = "large-v3-turbo",
        device: str = "cuda",
        compute_type: str = "float16",
    ) -> None:
        self._model = WhisperModel(
            model,
            device=device,
            compute_type=compute_type,
        )

    def transcribe(self, audio_path: Path) -> Transcription:
        """Преобразование аудио в текст"""
        segments, info = self._model.transcribe(
            str(audio_path),
            language="ru",
            vad_filter=True,
        )

        text = "\n".join(
            segment.text.strip()
            for segment in segments
            if segment.text.strip()
        )

        return Transcription(text=text, language=info.language, duration=info.duration)
