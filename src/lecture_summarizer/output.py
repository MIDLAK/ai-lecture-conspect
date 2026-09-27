from pathlib import Path
from .models import Summary


def save_markdown(summary: Summary, output_path: Path) -> None:
    """Сохранение результата суммаризации в файл"""
    output_path.write_text(summary.content,encoding="utf-8")
