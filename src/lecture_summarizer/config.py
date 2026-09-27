import os
from dataclasses import dataclass
from .models import Provider


@dataclass(frozen=True, slots=True)
class Settings:
    provider: Provider
    model: str

    whisper_model: str = "large-v3-turbo"
    whisper_device: str = "cuda"
    whisper_compute_type: str = "float16"

    gigachat_credentials: str | None = None
    gigachat_scope: str = "GIGACHAT_API_PERS"

    @classmethod
    def from_environment(cls, provider: Provider, model: str):
        """Получение параметров из переменных окружения"""
        return cls(
            provider=provider,
            model=model,
            whisper_model=os.getenv("WHISPER_MODEL", "large-v3-turbo"),
            whisper_device=os.getenv("WHISPER_DEVICE", "cuda"),
            whisper_compute_type=os.getenv("WHISPER_COMPUTE_TYPE", "float16"),
            gigachat_credentials=os.getenv("GIGACHAT_CREDENTIALS"),
            gigachat_scope=os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS"),
        )
