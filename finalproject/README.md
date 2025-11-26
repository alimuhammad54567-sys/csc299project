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

This folder is the clean final-code workspace. It contains a minimal, extendable CLI app with a simple JSON-backed store (`finalproject/data.json`) you can expand with features from task prototypes (GPX parsing, TUI, sync, etc.).

Next steps
- Merge useful code from `tasks1`..`tasks5` into `finalproject/` (GPX parsing, data models, utilities).
- Add tests, more CLI commands, and a migration path.
- New commands:
	- `menu`: interactive terminal menu to run common actions.
	- `agent`: a local keyword-based AI assistant that can run safe actions like `import parks`, `list parks`, `add park <name>` and `add visit to <park> party N`.

Notes on the `agent` LLM option

- The CLI supports adding personal notes for parks and visits. Use `--notes` when creating a park or visit to attach a short note.

Examples

```powershell
python -m finalproject.main add-park --name "My Park" --state "CA" --notes "Favorite campsite near the lake"
python -m finalproject.main visit-park --park "My Park" --date 2026-07-10 --party 3 --notes "Summer trip: bring camera"
python -m finalproject.main list-parks --show-notes
python -m finalproject.main list-visits --park "My Park"
```

Notes on the `agent` LLM option

The `agent` command has two modes:

1. **Restricted mode** (default): Works offline with rule-based parsing. Safely maps prompts to allowed actions only (list parks, import parks, add park, add visit).
2. **Chat mode** (`--chat` flag): Free-form conversation with the LLM. Answers any question without action restrictions.

Both modes require setting the `OPENAI_API_KEY` environment variable to use the LLM. If the key is not set, the agent falls back to local rule-based parsing.

### Setting your OpenAI API key

Get your API key from [OpenAI's API keys page](https://platform.openai.com/api-keys), then set it as an environment variable:

**PowerShell:**
```powershell
$env:OPENAI_API_KEY = 'your-key-here'
```

**Command Prompt (cmd):**
```cmd
set OPENAI_API_KEY=your-key-here
```

**Bash (Linux/Mac):**
```bash
export OPENAI_API_KEY='your-key-here'
```

### Usage examples

**Restricted mode (LLM-enabled, requires confirmation):**
```powershell
$env:OPENAI_API_KEY = 'your-key-here'
python -m finalproject.main agent --use-llm --prompt "add park Yellowstone WY"
```

**Chat mode (free-form conversation):**
```powershell
$env:OPENAI_API_KEY = 'your-key-here'
python -m finalproject.main agent --chat --prompt "best time to visit yosemite"
```

**Interactive chat mode:**
```powershell
$env:OPENAI_API_KEY = 'your-key-here'
python -m finalproject.main agent --chat
# Type your questions; type "exit" or "quit" to leave
```

### Security and privacy

- **Never commit your API key to git or share it with others.** The code does not store keys—it only reads from the `OPENAI_API_KEY` environment variable at runtime.
- In restricted mode, the agent shows the suggested action and asks for confirmation before executing. You accept responsibility for any API usage costs.
- If the API key is not set or the `openai` library is not installed, both modes fall back to safe, offline rule-based parsing.

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

Reset / clear data

If you want to restart the local dataset, use the `reset-data` command. This is destructive and will remove records from `finalproject/data.json`.

- Clear visits only (default):

```powershell
python -m finalproject.main reset-data --visits
```

- Clear parks and visits (removes all parks and visits):

```powershell
python -m finalproject.main reset-data --parks
```

- Clear everything and recreate an empty store:

```powershell
python -m finalproject.main reset-data --all
```

All commands will prompt for confirmation. To skip the confirmation (for scripted runs), pass `--yes`.

Interactive menu note

- The interactive `menu` exposes a "Clear data" option (Clear visits / Clear parks+visits / Clear all) so you can reset the local store without invoking the CLI flags directly. The menu will still ask for confirmation before performing destructive actions.



