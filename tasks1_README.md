# tasks1 — Simple CLI task prototype

This directory contains a minimal command-line tasks application that stores tasks in a JSON file.

Files:
- `tasks.py` — CLI program (Python 3). Supports adding, listing, and searching tasks.
- `tasks.json` — data file (initially an empty array). The CLI reads/writes this file.

Prerequisites:
- Python 3.6+ installed.

Quick usage:
1. From the tasks1 directory, run:
   ```bash
   python3 tasks.py add "Buy groceries" -d "Milk, eggs, bread" -t "shopping,errands"
   python3 tasks.py list
   python3 tasks.py search groceries
   ```

Command reference:
- `python3 tasks.py add <title> [-d DESCRIPTION] [-t TAGS]`
  - TAGS is a comma-separated list (e.g., `-t work,urgent`).
- `python3 tasks.py list`
  - Show all tasks.
- `python3 tasks.py search <query>`
  - Search title, description, and tags (case-insensitive substring match).

Installing into your repository and pushing to GitHub:
1. Clone your repo (if you haven't already):
   ```bash
   git clone https://github.com/alimuhammad54567-sys/csc299project.git
   cd csc299project
   ```
2. Create the tasks1 directory and add these files (or copy them in):
   ```bash
   mkdir -p tasks1
   # copy tasks.py, tasks.json, README.md into tasks1/
   ```
3. Add, commit, and push:
   ```bash
   git add tasks1/
   git commit -m "Add tasks1 CLI prototype (tasks.py, tasks.json, README)"
   git push origin main
   ```

Notes:
- `tasks.json` is created/updated by `tasks.py`. The script expects to be run from the `tasks1` directory (or run via full path).
- This is a prototype. If you'd like features such as edit/complete/delete, colored output, or tests, tell me which additions you want and I will provide updated code.