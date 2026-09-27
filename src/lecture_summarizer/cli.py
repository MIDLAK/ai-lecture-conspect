import argparse
from pathlib import Path
from .config import Settings
from .models import Provider
from .output import save_markdown
from .providers import ClaudeProvider, OpenAIProvider
from .summarization import Summarizer
from .transcription import WhisperTranscriber
from dotenv import load_dotenv

from .providers import (
    ClaudeProvider,
    GigaChatProvider,
    LLMProvider,
    OpenAIProvider,
)

DEFAULT_MODELS: dict[Provider, str] = {
    Provider.OPENAI: "gpt-5.6-luna",
    Provider.CLAUDE: "claude-sonnet-5",
    Provider.GIGACHAT: "GigaChat-2-Max"
}


def create_provider(settings: Settings) -> LLMProvider:
    """Выбор провайдера для суммаризации"""
    match settings.provider:
        case Provider.OPENAI:
            return OpenAIProvider(settings.model)

        case Provider.CLAUDE:
            return ClaudeProvider(settings.model)

        case Provider.GIGACHAT:
            if settings.gigachat_credentials is None:
                raise RuntimeError("GIGACHAT_CREDENTIALS не установлены")

            return GigaChatProvider(
                model=settings.model,
                credentials=settings.gigachat_credentials,
                scope=settings.gigachat_scope,
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Создание конспектов лекций из аудио в Markdown формате.",
    )

    parser.add_argument("audio", type=Path, help="Путь к файлу.")

    parser.add_argument(
        "--provider",
        type=Provider,
        choices=list(Provider),
        default=Provider.GIGACHAT,
    )

    parser.add_argument("--model", type=str, help="Модель провайдера")
    parser.add_argument("--output", type=Path, help="Файл для выдачи результата")

    return parser.parse_args()


def main():
    load_dotenv()

    args = parse_args()

    if not args.audio.is_file():
        raise FileNotFoundError(f"Файл с аудио не найден: {args.audio}")

    model = args.model or DEFAULT_MODELS[args.provider]

    settings = Settings.from_environment(provider=args.provider, model=model)

    print("Преобразование аудио в текст...")

    transcriber = WhisperTranscriber(
        model=settings.whisper_model,
        device=settings.whisper_device,
        compute_type=settings.whisper_compute_type,
    )

    transcription = transcriber.transcribe(args.audio)

    print(
        f"Преобразование завершилось: "
        f"{transcription.duration:.0f}s, "
        f"language={transcription.language}"
    )

    provider = create_provider(settings)

    summarizer = Summarizer(
        provider=provider,
        provider_type=settings.provider,
        model=settings.model,
    )

    print(f"Суммаризация моделью {settings.provider}/{settings.model}...")

    summary = summarizer.summarize(transcription.text)

    output_path = args.output or args.audio.with_suffix(".md")

    save_markdown(summary, output_path)

    print(f"Успешно, результат сохранён: {output_path}")


if __name__ == "__main__":
    main()
