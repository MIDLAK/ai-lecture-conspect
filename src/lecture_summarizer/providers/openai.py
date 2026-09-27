from openai import OpenAI
from .base import LLMProvider
from ..prompts import SYSTEM_PROMPT


class OpenAIProvider(LLMProvider):
    def __init__(self, model: str) -> None:
        self._client = OpenAI()
        self._model = model

    def summarize(self, text: str) -> str:
        response = self._client.responses.create(
            model=self._model,
            instructions=SYSTEM_PROMPT,
            input=text,
        )

        return response.output_text
