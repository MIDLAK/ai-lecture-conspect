from .models import Provider, Summary
from .providers import LLMProvider


class Summarizer:
    def __init__(self,provider: LLMProvider, provider_type: Provider, model: str) -> None:
        self._provider = provider
        self._provider_type = provider_type
        self._model = model

    def summarize(self, text: str) -> Summary:
        """Получение результатов суммаризации аудио лекции"""
        content = self._provider.summarize(text)
        return Summary(content=content, provider=self._provider_type, model=self._model)
