# Final Project: National Park Tracker (Terminal)

This is the final project scaffold for a terminal-based National Park Tracker.

Quick start

1. Create a virtual environment and install requirements:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r finalproject/requirements.txt
```

2. Initialize the database and view CLI help:

```powershell
python -m finalproject.main --help
```

Purpose

This folder is the clean final-code workspace. It contains a minimal, extendable CLI app with a SQLite backend you can expand with features from task prototypes (GPX import, TUI, sync, etc.).

Next steps
- Merge useful code from `tasks1`..`tasks5` into `finalproject/` (GPX parsing, data models, utilities).
- Add tests, more CLI commands, and a migration path.
- New commands:
	- `menu`: interactive terminal menu to run common actions.
	- `agent`: a local keyword-based AI assistant that can run safe actions like `import parks`, `list parks`, `add park <name>` and `add visit to <park> party N`.

Notes on the `agent` LLM option

- The `agent` still works offline with rule-based parsing. For more natural responses you can enable an external LLM using the `--use-llm` flag. This will attempt to call OpenAI if you set the `OPENAI_API_KEY` environment variable and install the `openai` package.
- Example (one-shot LLM-enabled):

```powershell
$env:OPENAI_API_KEY = 'sk-xxxx'
python -m finalproject.main agent --use-llm --prompt "Find parks in CA and plan a 3-person visit to Yosemite next July"
```

Security and safety: the LLM integration is intentionally limited — the agent only maps LLM text to a small set of allowed, safe actions (import parks, list parks, add park, add visit). You must provide your own API key and accept any costs from the provider.

Important: API key usage and privacy

- You must provide your own API key via the `OPENAI_API_KEY` environment variable. The project will read the key from your environment at runtime and will not store or transmit your key elsewhere from your machine. Do not paste or share your API key in chat or with others.
- The agent will show the LLM's suggested action and ask you to confirm before executing anything. If the key is not present or the `openai` library is not installed, the agent falls back to the safe, local rule-based parser.

Examples

```powershell
python -m finalproject.main menu
python -m finalproject.main agent --prompt "list parks"
```

Visit tracking

- Mark a park visited (creates a visit record):

```powershell
python -m finalproject.main visit-park --park "Yellowstone" --date 2026-07-10 --party 3 --notes "Summer trip"
```

- List only visited parks:

```powershell
python -m finalproject.main list-parks --visited
```

- List only parks you haven't visited yet:

```powershell
python -m finalproject.main list-parks --unvisited
```

- Show personal notes for parks:

```powershell
python -m finalproject.main list-parks --show-notes
```

- Add or update a personal note for a park:

```powershell
python -m finalproject.main note-park --park "Yosemite" --note "Great hike at Upper Falls; bring water."
```


