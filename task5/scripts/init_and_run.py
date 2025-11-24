#!/usr/bin/env python3
"""Initialize project structure and run scripts, storing results in JSON.

Usage examples (PowerShell):
  python .\scripts\init_and_run.py init
  python .\scripts\init_and_run.py run --commands "Write-Output 'hello'" "Get-ChildItem"
  python .\scripts\init_and_run.py run --file commands.json --output run_results.json
  python .\scripts\init_and_run.py run-plan --plan tasks5/.github/prompts/speckit.plan.prompt.md

The script runs commands via PowerShell and records stdout/stderr/returncode.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime


def init_project(base_dir: str):
    scripts_dir = os.path.join(base_dir, "scripts")
    examples_dir = os.path.join(scripts_dir, "examples")
    os.makedirs(examples_dir, exist_ok=True)

    # Add a sample PowerShell script
    sample_path = os.path.join(examples_dir, "say_hello.ps1")
    if not os.path.exists(sample_path):
        with open(sample_path, "w", encoding="utf-8") as f:
            f.write("Write-Output 'Hello from sample script'\n")

    print(f"Initialized directories: {scripts_dir} and {examples_dir}")
    print(f"Created sample script: {sample_path}")


def load_commands_from_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    raise ValueError("Commands JSON must be a list of command strings")


def extract_commands_from_plan(plan_path: str):
    # Extract fenced code blocks from a markdown-like plan file.
    if not os.path.exists(plan_path):
        raise FileNotFoundError(plan_path)
    with open(plan_path, "r", encoding="utf-8") as f:
        text = f.read()

    commands = []
    in_block = False
    block_lines = []
    fence_lang = None
    for line in text.splitlines():
        if line.strip().startswith("```"):
            if not in_block:
                in_block = True
                fence_lang = line.strip()[3:].strip().lower()
                block_lines = []
            else:
                # end of block
                in_block = False
                block_text = "\n".join(block_lines).strip()
                if block_text:
                    # If the block is a shell/powershell block, split into commands by newline
                    commands.extend([l for l in block_text.splitlines() if l.strip()])
                fence_lang = None
                block_lines = []
        elif in_block:
            block_lines.append(line)

    return commands


def run_command_powershell(command: str, timeout: int = 300):
    # Run a command through PowerShell to be consistent with user's environment.
    proc = subprocess.run([
        "powershell",
        "-NoProfile",
        "-NonInteractive",
        "-Command",
        command
    ], capture_output=True, text=True, timeout=timeout)
    return {
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


def run_commands(commands, output_path: str):
    results = []
    for cmd in commands:
        print(f"Running: {cmd}")
        try:
            res = run_command_powershell(cmd)
        except Exception as e:
            res = {
                "command": cmd,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
        results.append(res)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Wrote results to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Initialize project and run scripts, saving results to JSON")
    sub = parser.add_subparsers(dest="cmd")

    p_init = sub.add_parser("init", help="Initialize scripts folders and add sample scripts")

    p_run = sub.add_parser("run", help="Run provided commands or commands listed in a JSON file")
    p_run.add_argument("--commands", nargs="*", help="Commands to run (each treated as a single PowerShell command)")
    p_run.add_argument("--file", help="Path to JSON file containing a list of command strings")
    p_run.add_argument("--output", default="run_results.json", help="Output JSON file to store results")

    p_plan = sub.add_parser("run-plan", help="Extract and run commands from a plan file (fenced code blocks)")
    p_plan.add_argument("--plan", required=True, help="Path to the plan file to extract commands from")
    p_plan.add_argument("--output", default="run_results.json", help="Output JSON file to store results")

    p_uv_init = sub.add_parser("uv-init", help="Attempt to initialize project using 'uv init' CLI")
    p_uv_init.add_argument("--output", default="uv_init_results.json", help="Output JSON file to store results")

    p_uv_run = sub.add_parser("uv-run", help="Attempt to run a script using 'uv run <name>' CLI")
    p_uv_run.add_argument("--script", required=True, help="Script or task name to run via 'uv run'")
    p_uv_run.add_argument("--output", default="uv_run_results.json", help="Output JSON file to store results")

    args = parser.parse_args()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Check Python version requirement (user requested >= 3.14)
    min_major, min_minor = 3, 14
    ver = sys.version_info
    if (ver.major, ver.minor) < (min_major, min_minor):
        print(f"Warning: Python {min_major}.{min_minor}+ requested but running {ver.major}.{ver.minor}. Continuing anyway.")

    if args.cmd == "init":
        init_project(base_dir)
        return

    if args.cmd == "run":
        if args.file:
            commands = load_commands_from_file(args.file)
        else:
            commands = args.commands or []
        if not commands:
            print("No commands provided. Use --commands or --file.")
            sys.exit(2)
        run_commands(commands, args.output)
        return

    if args.cmd == "run-plan":
        commands = extract_commands_from_plan(args.plan)
        if not commands:
            print("No commands found in plan file.")
            sys.exit(1)
        run_commands(commands, args.output)
        return

    if args.cmd == "uv-init":
        # Try to run `uv init` via PowerShell
        cmd = "uv init"
        print(f"Attempting to run: {cmd}")
        try:
            res = run_command_powershell(cmd)
        except Exception as e:
            res = {"command": cmd, "error": str(e), "timestamp": datetime.utcnow().isoformat() + "Z"}
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump([res], f, indent=2, ensure_ascii=False)
        print(f"Wrote uv init result to {args.output}")
        return

    if args.cmd == "uv-run":
        # Run `uv run <script>` via PowerShell
        script_name = args.script
        cmd = f"uv run {script_name}"
        print(f"Attempting to run: {cmd}")
        try:
            res = run_command_powershell(cmd)
        except Exception as e:
            res = {"command": cmd, "error": str(e), "timestamp": datetime.utcnow().isoformat() + "Z"}
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump([res], f, indent=2, ensure_ascii=False)
        print(f"Wrote uv run result to {args.output}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
