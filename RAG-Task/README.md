# RAG-Task

This folder contains code for a Retrieval-Augmented Generation (RAG) example and related tasks.

## Contents
- `app.py` — likely a web app or service entrypoint (check whether it uses Flask/FastAPI).
- `litellm_task.py` — a lightweight LLM wrapper or example usage.
- `rag_task.py` — RAG-specific orchestration.
- `requirements.txt` — Python dependencies for this module.
- `example.env` — example environment variables (copy and fill in secrets/API keys as needed).

---

## Prerequisites
- Linux with Bash (these instructions assume bash).
- Python 3.8+.
- Git (if you need to clone the repository).

## Quick setup (one-off)
If you don't yet have the repository locally:

```bash
# clone the repository (replace <repo-url> with your repo URL)
git clone <repo-url>
cd "Gen-AI-LLM Tasks/RAG-Task"
```
## Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Environment variables
Copy and edit the example env file:

```bash
cp example.env .env
# edit .env and add any API keys (e.g., OPENAI_API_KEY, VECTOR_DB_URL, etc.)
```

## Running the project
Depending on the intended entry point:

- If `app.py` is a web app (Flask/FastAPI), run:

```bash
python app.py
# or if using flask CLI
# FLASK_APP=app.py flask run
```

- Run RAG orchestration:

```bash
python rag_task.py
```

- Run the lite LLM example:

```bash
python litellm_task.py
```

If a script requires extra flags, run `--help` for usage:

```bash
python app.py --help
```

## Notes about web apps
If `app.py` starts a server, it will usually print the host/port. If needed, set environment variables like `HOST` and `PORT` in `.env` or via the shell.

## Troubleshooting
- If package installation fails with compilation errors, install system build tools (e.g., `sudo apt-get install build-essential libssl-dev libffi-dev python3-dev`) and re-run `pip install`.
- If the app can't connect to a vector DB or external service, verify credentials in `.env` and network access.

## Testing & Development
- Add and run `pytest` tests if present.

---

Last updated: 2025-10-29
