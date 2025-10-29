# OpenAIAssistantTask

This folder contains a set of assistant helper scripts and a CLI for the OpenAI-based assistant tasks.

## Contents
- `cli_assistant.py` — CLI entry for the assistant.
- `main_task.py` — main orchestration or example runner.
- `scraping_script.py` — a helper script to scrape or gather content (if used).
- `requirements.txt` — Python dependencies for this module.
- `example.env` — example environment variables (copy and fill in secrets/API keys as needed).

---

## Prerequisites
- Linux/macOS with Bash (these instructions assume bash).
- Python 3.8+.
- Git (to clone the repo if necessary).

## Quick setup (one-off)
If you don't yet have the repository locally:

```bash
# clone the repository (replace <repo-url> with your repo URL)
git clone <repo-url>
cd "Gen-AI-LLM Tasks/OpenAIAssistantTask"
```

## Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Environment variables
Copy the `example.env` to `.env` and populate keys (for example `OPENAI_API_KEY`):

```bash
cp example.env .env
# edit .env
```

Alternatively export keys in your shell before running scripts:

```bash
export OPENAI_API_KEY="your_key_here"
export LANGFUSE_SECRET_KEY="your_key_here"
export LANGFUSE_PUBLIC_KEY="your_key_here"

```

## Run the scripts
- CLI assistant (interactive):

```bash
python cli_assistant.py
```

- Main task/orchestrator:

```bash
python main_task.py
```

- Scraping helper (if applicable):

```bash
python scraping_script.py
```

If any script supports flags, run `--help` to get usage details:

```bash
python cli_assistant.py --help
```

## Tests / Development
If you want to add tests or run quick checks, install `pytest` in the venv and run `pytest`.

## Troubleshooting
- If you get errors installing packages, look at the failing package and install any required system libs (e.g., `libssl-dev`, `build-essential`).
- Ensure you activated the venv before running the scripts.
- If the assistant relies on external APIs, verify network access and API key validity.

## Notes
- Keep a separate venv per task folder to isolate dependencies.

---

Last updated: 2025-10-29
