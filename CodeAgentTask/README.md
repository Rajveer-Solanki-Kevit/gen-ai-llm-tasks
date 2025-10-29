# CodeAgentTask

This folder contains the Code Agent sample tasks and generator/tester utilities.

## Contents
- `cli_agent.py` — CLI script for the agent (interactive CLI).
- `main_task.py` — streamlit web application of agent.
- `codegen/` — generator and tester utilities (`generator.py`, `tester.py`).
- `requirements.txt` — Python dependencies for this module.
- `example.env` — example environment variables (copy and fill in secrets/API keys as needed).

---

## Prerequisites
- Python 3.8+ (adjust if project requires a different minor version).
- Git (to clone the repo if you haven't already).

## Quick setup (one-off)
If you don't yet have the repository locally:

```bash
# clone the repository (replace <repo-url> with your repo URL)
git clone <repo-url>
cd "Gen-AI-LLM Tasks/CodeAgentTask"
```

## Create and activate a virtual environment (recommended)

```bash
# create venv in project folder
python3 -m venv .venv
# activate it (bash)
source .venv/bin/activate
# upgrade pip
python -m pip install --upgrade pip
# install requirements for this folder
pip install -r requirements.txt
```

Notes:
- The venv is created inside the folder as `.venv`. You can choose a different name if you prefer.
- To deactivate later: `deactivate`.

## Environment variables
Copy the example and populate any API keys or secrets:

```bash
cp example.env .env
# then edit .env with your secrets (e.g. OPENAI_API_KEY, etc.)
```

Some scripts may read `.env` automatically; otherwise export needed variables in your shell:

```bash
export OPENAI_API_KEY="your_key_here"
```

## Run the code
Choose an entry point depending on what you want to do.

- Run the CLI agent:

```bash
python3 cli_agent.py
```

- Run the main task/orchestrator:

```bash
streamlit run main_task.py
```

- Use generator/tester utilities (for development):

```bash
# run generator
python3 -m codegen.generator
# run tester
python3 -m codegen.tester
```

If any script requires flags or options, run `--help` on the script to discover usage, for example:

```bash
python3 cli_agent.py --help
```

## Notes
- Keep virtual environments per-folder to avoid dependency collisions across the three tasks.

---

Last updated: 2025-10-29
