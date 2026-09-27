from gigachat import GigaChat

from ..prompts import SYSTEM_PROMPT
from .base import LLMProvider


class GigaChatProvider(LLMProvider):
    def __init__(
        self,
        model: str,
        credentials: str,
        scope: str,
    ) -> None:
        self._client = GigaChat(
            credentials=credentials,
            scope=scope,
            base_url="https://api.giga.chat/v1",
            model=model,
            verify_ssl_certs=False,
            timeout=6000
        )
        self._model = model

    def _extract_text(self, content) -> str:
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts: list[str] = []
            for block in content:
                if isinstance(block, dict):
                    parts.append(block.get("text", ""))
                else:
                    text = getattr(block, "text", None)
                    if text:
                        parts.append(text)
            return "".join(parts)
        return str(content)


    def summarize(self, text: str) -> str:
        response = self._client.chat.create(
            {
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": text},
                ]
            }
        )
        return self._extract_text(response.messages[0].content)
