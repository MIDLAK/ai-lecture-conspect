# ai-lecture-conspect

CLI-утилита для автоматической транскрибации и суммаризации лекций:
аудио → текст (Whisper) → markdown-конспект.

## Зачем

Во время лекции трудно успевать записывать, а переслушивать часовую запись
ради пары мыслей, как правило, никто не станет. Утилита превращает аудио в компактную
текстовую выжимку в формате Markdown.

## Требования

- Python ≥ 3.12
- CUDA ≥ 12 (для GPU-инференса Whisper)
- ffmpeg
- API ключ GigaChat, OpenAI или Claude


## Установка

```bash
python -m venv .venv
source .venv/bin/activate

pip install -e .
```

## Настройка `.env`

Создайте `.env` в корне проекта и заполните переменные по примеру env.example

Если нет GPU, укажите в `.env`:

```env
WHISPER_DEVICE=cpu
WHISPER_COMPUTE_TYPE=int8
```

## Запуск

```bash
ai-lecture-conspect <filepath.m4a> --provider <llm_provider> --model <provider_model> --output <output.md>
```

Пример:

```bash
ai-lecture-conspect lecture-01.m4a --provider gigachat --output lecture-01.md
```

### Флаги

| Флаг | Обязателен | Описание |
|------|:----------:|----------|
| `<filepath>` | да | Путь к аудио/видеофайлу |
| `--provider` | нет | Провайдер LLM (по умолчанию: `gigachat`) |
| `--output` | нет | Путь к `.md`-файлу с результатом |
| `--model` | нет | Имя модели (по умолчанию `GigaChat-2-Max`) |

## Типичные ошибки 

### `Library libcublas.so.12 is not found or cannot be loaded`

CUDA-библиотеки не попадают в `LD_LIBRARY_PATH`. Выполните:

```bash
export LD_LIBRARY_PATH=$(
    python3 -c "import nvidia.cublas.lib, nvidia.cudnn.lib; \
                print(nvidia.cublas.lib.__path__[0] + ':' + nvidia.cudnn.lib.__path__[0])"
):$LD_LIBRARY_PATH
```

Чтобы не вводить каждый раз — добавьте строку в `~/.bashrc` или `~/.zshrc`.
