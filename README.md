## Code Generator

Code Generator is a LangGraph-based multi-node pipeline that generates Python code from a user task.

The graph includes three nodes:
- architect: rewrites the request into a technical implementation plan
- coder: generates the code
- tester: writes a bug report when code quality is insufficient

The Streamlit chat UI currently returns only `coder_output` as the final assistant result.

## Requirements

- Python 3.12+
- OpenAI API key

## 1. Clone and enter project

```bash
git clone https://github.com/vladkuz54/code-generator.git
cd code-generator
```

## 2. Create and activate virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies

Recommended (from `pyproject.toml`):

```bash
pip install -e .
```

Alternative (from `requirements.txt`):

```bash
pip install -r requirements.txt
```

## 4. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Notes:
- Keep `.env` in the same directory as `main.py` and `chat.py`.
- Do not commit `.env` to git.

## 5. Run the project

### Option A: CLI run

```bash
python main.py
```

This runs one sample request through the graph and prints the resulting state.

### Option B: Streamlit chat UI

```bash
python -m streamlit run chat.py
```

Then open the local URL shown in terminal (usually `http://localhost:8501`).

## How the UI works

- Left panel: chat conversation
- Right panel: detailed node-by-node events from the graph stream
- Final assistant message: only generated code (`coder_output`)

## Project structure

```text
chat.py                  # Streamlit UI
main.py                  # CLI entry point
graph/
	graph.py               # LangGraph workflow definition
	state.py               # graph state schema
	nodes/
		architect.py
		coder.py
		tester.py
	chains/
		architect_chain.py
		coder_chain.py
		tester_chain.py
		code_grader_chain.py
```

## Troubleshooting

### Error: OpenAIError api_key client option must be set

Cause:
- `OPENAI_API_KEY` is missing or not loaded.

Fix:
- Verify `.env` exists in project root.
- Verify it contains `OPENAI_API_KEY=...`.
- Restart terminal after changing environment setup.

### Error: streamlit is not recognized

Cause:
- Streamlit is not available in the current shell context.

Fix:
- Activate virtual environment.
- Run Streamlit as module:

```bash
python -m streamlit run chat.py
```

### Graph does not start or exits immediately

Fix:
- Ensure dependencies are installed in the same active venv.
- Run `python main.py` first to confirm core graph works.

## Development notes

- Formatting tools listed in dependencies: `black`, `isort`.
- Main graph decision logic is in `graph/graph.py` (`decide_to_transform`).
