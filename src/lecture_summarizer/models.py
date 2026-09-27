from dataclasses import dataclass
from enum import StrEnum


class Provider(StrEnum):
    OPENAI = "openai"
    CLAUDE = "claude"
    GIGACHAT = "gigachat"


@dataclass
class Transcription:
    text: str
    language: str
    duration: float


@dataclass
class Summary:
    content: str
    provider: Provider
    model: str
