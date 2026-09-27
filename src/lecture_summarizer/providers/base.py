from abc import ABC, abstractmethod


class LLMProvider(ABC):

    @abstractmethod
    def summarize(self, text: str) -> str:
        """Получение Markdown summary из передаваемого текста"""
        raise NotImplementedError
