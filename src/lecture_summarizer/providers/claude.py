import anthropic
from .base import LLMProvider
from ..prompts import SYSTEM_PROMPT


class ClaudeProvider(LLMProvider):
    def __init__(self, model: str) -> None:
        self._client = anthropic.Anthropic()
        self._model = model

    def summarize(self, text: str) -> str:
        response = self._client.messages.create(
            model=self._model,
            max_tokens=16_000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": text}],
        )

        return "".join(
            block.text
            for block in response.content
            if block.type == "text"
        )
