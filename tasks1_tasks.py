#!/usr/bin/env python3

import argparse
import json
import os
import datetime
import textwrap

DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def next_id(tasks):
    if not tasks:
        return 1
    return max(t.get("id", 0) for t in tasks) + 1

def add_task(title, description, tags):
    tasks = load_tasks()
    task = {
        "id": next_id(tasks),
        "title": title,
        "description": description,
        "tags": tags,
        "completed": False,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task #{task['id']}: {task['title']}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for t in tasks:
        tags = ",".join(t.get("tags", [])) if t.get("tags") else ""
        print(f"#{t.get('id')} {'[x]' if t.get('completed') else '[ ]'} {t.get('title')}\n  tags: {tags}\n  created: {t.get('created_at')}\n  desc: {textwrap.shorten(t.get('description',''), width=120)}\n")

def search_tasks(query):
    q = query.lower()
    tasks = load_tasks()
    results = []
    for t in tasks:
        hay = " ".join([
            str(t.get("title", "")),
            str(t.get("description", "")),
            " ".join(t.get("tags", [])) if t.get("tags") else "",
        ]).lower()
        if q in hay:
            results.append(t)
    if not results:
        print("No matching tasks.")
        return
    for t in results:
        tags = ",".join(t.get("tags", [])) if t.get("tags") else ""
        print(f"#{t.get('id')} {'[x]' if t.get('completed') else '[ ]'} {t.get('title')}\n  tags: {tags}\n  desc: {t.get('description')}\n")

def parse_tags(s):
    if not s:
        return []
    return [x.strip() for x in s.split(",") if x.strip()]

def main():
    parser = argparse.ArgumentParser(description="Simple tasks CLI storing data in tasks1/tasks.json")
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title", help="Task title")
    p_add.add_argument("-d", "--description", default="", help="Task description")
    p_add.add_argument("-t", "--tags", default="", help="Comma-separated tags")

    p_list = sub.add_parser("list", help="List all tasks")

    p_search = sub.add_parser("search", help="Search tasks by text")
    p_search.add_argument("query", help="Search query")

    args = parser.parse_args()

    if args.cmd == "add":
        add_task(args.title, args.description, parse_tags(args.tags))
    elif args.cmd == "list":
        list_tasks()
    elif args.cmd == "search":
        search_tasks(args.query)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()