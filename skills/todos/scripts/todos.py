#!/usr/bin/env python3
"""
Todos Manager - Automatic task tracking for projects

Usage:
    todos.py check [--root PATH]       Check if TODOS.md exists, show summary
    todos.py init [--root PATH]        Create TODOS.md if not exists
    todos.py add TASK [--root PATH]    Add a new task
    todos.py start TASK [--root PATH]  Mark task as in-progress
    todos.py done TASK [--root PATH]   Mark task as completed
    todos.py list [--root PATH]        List all tasks by status
    todos.py search QUERY [--root PATH] Search for a task
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Tuple

TODOS_FILENAMES = ["TODOS.md", "todos.md", ".todos.md"]

TEMPLATE = """# Project Todos

> Auto-managed by AI assistant. Last updated: {date}

## In Progress
<!-- Tasks currently being worked on -->

## Pending
<!-- Tasks waiting to be done -->

## Completed
<!-- Finished tasks with completion dates -->

---

## Task Log

| Task | Status | Created | Completed | Notes |
|------|--------|---------|-----------|-------|

"""

def find_todos_file(root: Path) -> Optional[Path]:
    """Find existing TODOS.md file in various naming conventions."""
    for name in TODOS_FILENAMES:
        path = root / name
        if path.exists():
            return path
    return None

def get_todos_path(root: Path) -> Path:
    """Get the path for TODOS.md (existing or default for new)."""
    existing = find_todos_file(root)
    if existing:
        return existing
    return root / "TODOS.md"

def init_todos(root: Path) -> Tuple[bool, str]:
    """Initialize TODOS.md if it doesn't exist."""
    existing = find_todos_file(root)
    if existing:
        return False, f"TODOS.md already exists at: {existing}"
    
    todos_path = root / "TODOS.md"
    content = TEMPLATE.format(date=datetime.now().strftime("%Y-%m-%d"))
    todos_path.write_text(content)
    return True, f"Created: {todos_path}"

def read_todos(root: Path) -> Optional[str]:
    """Read TODOS.md content."""
    path = find_todos_file(root)
    if path:
        return path.read_text()
    return None

def parse_tasks(content: str) -> dict:
    """Parse tasks from TODOS.md content."""
    tasks = {
        "pending": [],
        "in_progress": [],
        "completed": [],
        "blocked": [],
        "cancelled": []
    }
    
    # Match task lines: - [x] task text (optional date)
    pattern = r"^\s*-\s*\[(.)\]\s*(.+?)(?:\s*\(([^)]+)\))?$"
    
    for line in content.split("\n"):
        match = re.match(pattern, line)
        if match:
            marker, text, date = match.groups()
            task_info = {"text": text.strip(), "date": date}
            
            if marker == " ":
                tasks["pending"].append(task_info)
            elif marker == "~":
                tasks["in_progress"].append(task_info)
            elif marker == "x":
                tasks["completed"].append(task_info)
            elif marker == "!":
                tasks["blocked"].append(task_info)
            elif marker == "-":
                tasks["cancelled"].append(task_info)
    
    return tasks

def task_exists(content: str, task_query: str) -> Optional[Tuple[str, str]]:
    """Check if a similar task exists. Returns (status, full_text) or None."""
    query_lower = task_query.lower()
    pattern = r"^\s*-\s*\[(.)\]\s*(.+?)(?:\s*\(([^)]+)\))?$"
    
    for line in content.split("\n"):
        match = re.match(pattern, line)
        if match:
            marker, text, _ = match.groups()
            if query_lower in text.lower():
                status_map = {" ": "pending", "~": "in_progress", "x": "completed", "!": "blocked", "-": "cancelled"}
                return (status_map.get(marker, "unknown"), text.strip())
    return None

def add_task(root: Path, task: str) -> Tuple[bool, str]:
    """Add a new task to TODOS.md."""
    path = find_todos_file(root)
    if not path:
        return False, "TODOS.md not found. Run 'init' first."
    
    content = path.read_text()
    
    # Check if task already exists
    existing = task_exists(content, task)
    if existing:
        status, text = existing
        return False, f"Similar task already exists [{status}]: {text}"
    
    # Find ## Pending section and add task after it
    date_str = datetime.now().strftime("%Y-%m-%d")
    new_task = f"- [ ] {task} (added: {date_str})"
    
    # Insert after "## Pending" line and its comment
    lines = content.split("\n")
    new_lines = []
    inserted = False
    skip_until = -1
    
    for i, line in enumerate(lines):
        if i < skip_until:
            continue
        new_lines.append(line)
        if not inserted and line.strip() == "## Pending":
            # Find next non-comment, non-empty line or section
            j = i + 1
            while j < len(lines) and (lines[j].strip().startswith("<!--") or lines[j].strip() == ""):
                new_lines.append(lines[j])
                j += 1
            new_lines.append(new_task)
            inserted = True
            skip_until = j  # Skip already processed lines
    
    # Update last modified date
    final_content = "\n".join(new_lines)
    final_content = re.sub(
        r"Last updated: \d{4}-\d{2}-\d{2}",
        f"Last updated: {date_str}",
        final_content
    )
    
    path.write_text(final_content)
    return True, f"Added task: {task}"

def update_task_status(root: Path, task_query: str, new_status: str) -> Tuple[bool, str]:
    """Update a task's status."""
    path = find_todos_file(root)
    if not path:
        return False, "TODOS.md not found."
    
    content = path.read_text()
    query_lower = task_query.lower()
    
    status_markers = {"pending": " ", "in_progress": "~", "completed": "x", "blocked": "!", "cancelled": "-"}
    new_marker = status_markers.get(new_status, " ")
    
    lines = content.split("\n")
    updated = False
    updated_task = ""
    
    for i, line in enumerate(lines):
        match = re.match(r"^(\s*-\s*\[)(.)(]\s*)(.+)$", line)
        if match and query_lower in match.group(4).lower():
            prefix, _, middle, task_text = match.groups()
            
            # Add completion date if marking as done
            date_str = datetime.now().strftime("%Y-%m-%d")
            if new_status == "completed":
                # Remove old date markers and add completion date
                task_text = re.sub(r"\s*\((?:added|started|completed):[^)]+\)", "", task_text)
                task_text = f"{task_text.strip()} (completed: {date_str})"
            elif new_status == "in_progress":
                task_text = re.sub(r"\s*\(added:[^)]+\)", "", task_text)
                task_text = f"{task_text.strip()} (started: {date_str})"
            
            lines[i] = f"{prefix}{new_marker}{middle}{task_text}"
            updated = True
            updated_task = task_text.strip()
            break
    
    if updated:
        content = "\n".join(lines)
        date_str = datetime.now().strftime("%Y-%m-%d")
        content = re.sub(
            r"Last updated: \d{4}-\d{2}-\d{2}",
            f"Last updated: {date_str}",
            content
        )
        path.write_text(content)
        return True, f"Updated to [{new_status}]: {updated_task}"
    
    return False, f"Task not found: {task_query}"

def list_tasks(root: Path) -> str:
    """List all tasks with their status."""
    content = read_todos(root)
    if not content:
        return "No TODOS.md found."
    
    tasks = parse_tasks(content)
    
    output = []
    output.append("=== TODOS Summary ===\n")
    
    if tasks["in_progress"]:
        output.append("🔄 In Progress:")
        for t in tasks["in_progress"]:
            output.append(f"  - {t['text']}")
    
    if tasks["pending"]:
        output.append("\n📋 Pending:")
        for t in tasks["pending"]:
            output.append(f"  - {t['text']}")
    
    if tasks["blocked"]:
        output.append("\n🚫 Blocked:")
        for t in tasks["blocked"]:
            output.append(f"  - {t['text']}")
    
    if tasks["completed"]:
        output.append(f"\n✅ Completed ({len(tasks['completed'])} tasks)")
        # Show last 5 completed
        for t in tasks["completed"][-5:]:
            date = f" ({t['date']})" if t['date'] else ""
            output.append(f"  - {t['text']}{date}")
    
    # Summary counts
    output.append("\n---")
    output.append(f"Total: {len(tasks['pending'])} pending, {len(tasks['in_progress'])} in progress, {len(tasks['completed'])} completed")
    
    return "\n".join(output)

def check_todos(root: Path) -> str:
    """Quick check of TODOS.md status."""
    path = find_todos_file(root)
    if not path:
        return "NO_TODOS_FILE"
    
    content = path.read_text()
    tasks = parse_tasks(content)
    
    return f"EXISTS|pending:{len(tasks['pending'])}|in_progress:{len(tasks['in_progress'])}|completed:{len(tasks['completed'])}"

def search_task(root: Path, query: str) -> str:
    """Search for a task."""
    content = read_todos(root)
    if not content:
        return "No TODOS.md found."
    
    result = task_exists(content, query)
    if result:
        status, text = result
        return f"FOUND|{status}|{text}"
    return "NOT_FOUND"

def main():
    parser = argparse.ArgumentParser(description="Todos Manager")
    parser.add_argument("command", choices=["check", "init", "add", "start", "done", "list", "search"])
    parser.add_argument("task", nargs="?", help="Task text or search query")
    parser.add_argument("--root", default=".", help="Project root directory")
    
    args = parser.parse_args()
    root = Path(args.root).resolve()
    
    if args.command == "check":
        print(check_todos(root))
    
    elif args.command == "init":
        created, msg = init_todos(root)
        print(msg)
        sys.exit(0 if created else 1)
    
    elif args.command == "add":
        if not args.task:
            print("Error: Task text required")
            sys.exit(1)
        success, msg = add_task(root, args.task)
        print(msg)
        sys.exit(0 if success else 1)
    
    elif args.command == "start":
        if not args.task:
            print("Error: Task query required")
            sys.exit(1)
        success, msg = update_task_status(root, args.task, "in_progress")
        print(msg)
        sys.exit(0 if success else 1)
    
    elif args.command == "done":
        if not args.task:
            print("Error: Task query required")
            sys.exit(1)
        success, msg = update_task_status(root, args.task, "completed")
        print(msg)
        sys.exit(0 if success else 1)
    
    elif args.command == "list":
        print(list_tasks(root))
    
    elif args.command == "search":
        if not args.task:
            print("Error: Search query required")
            sys.exit(1)
        print(search_task(root, args.task))

if __name__ == "__main__":
    main()
