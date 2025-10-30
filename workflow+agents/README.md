# RAG-Task

This folder contains code for workflow+agents and langgraph example and related tasks.

## Contents
- `app.py` — main script.
- `requirements.txt` — Python dependencies for this module.
- `example.env` — example environment variables (copy and fill in secrets/API keys as needed).

---

## Prerequisites
- Python 3.8+.
- Git (if you need to clone the repository).

## Quick setup (one-off)
If you don't yet have the repository locally:

```bash
# clone the repository (replace <repo-url> with your repo URL)
git clone <repo-url>
cd "Gen-AI-LLM Tasks/workflow+agents"
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

- If `app.py` script, run:

```bash
python3 app.py 
```

Last updated: 2025-10-30
