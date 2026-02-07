---
name: todos
description: Automatic todo tracking and task management for projects
---

# Todos Skill - Automatic Task Management

This skill provides **automatic** todo tracking that integrates into every work session. The AI proactively manages todos without explicit user requests.

## When This Skill Activates

**AUTOMATIC ACTIVATION** - This skill should be mentally activated at the START of every task:
- When starting any new work in a project
- When the user asks to implement/fix/change anything
- Before beginning any coding task
- When reviewing or continuing previous work

## Core Workflow

### Phase 1: Project Todo Check (ALWAYS RUN FIRST)

**Before doing ANY work, check for existing todos file:**

```bash
# Check in project root (not opencode config)
ls -la ./TODOS.md 2>/dev/null || ls -la ./todos.md 2>/dev/null || ls -la ./.todos.md 2>/dev/null
```

**If NO todos file exists:**
1. Create `TODOS.md` in the project root
2. Initialize with standard template (see below)
3. Inform user: "Created TODOS.md for task tracking"

**If todos file EXISTS:**
1. Read the current todos
2. Check if current task is already listed
3. Update status if task is in progress or completed

### Phase 2: Task Registration

When starting a new task:

1. **Check if task already exists** in TODOS.md
2. **If NOT exists**: Add new task entry with status `[ ]` (pending)
3. **If EXISTS as completed** `[x]`: Inform user "This task was already completed on [date]"
4. **If EXISTS as pending** `[ ]`: Mark as in-progress `[~]` and continue

### Phase 3: Task Completion

When finishing a task:

1. Update task status from `[ ]` or `[~]` to `[x]`
2. Add completion timestamp
3. Optionally add brief completion notes

## TODOS.md Template

```markdown
# Project Todos

> Auto-managed by AI assistant. Last updated: YYYY-MM-DD

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

```

## Task Entry Format

### Status Markers
- `[ ]` - Pending (not started)
- `[~]` - In Progress (currently working)
- `[x]` - Completed
- `[!]` - Blocked (has dependencies/issues)
- `[-]` - Cancelled/Skipped

### Example Entries

```markdown
## In Progress
- [~] Implement user authentication (started: 2024-01-15)

## Pending
- [ ] Add password reset flow
- [ ] Write unit tests for auth module
- [!] Deploy to staging (blocked: waiting for CI fix)

## Completed
- [x] Set up project structure (2024-01-10)
- [x] Configure database connection (2024-01-12)
- [-] Old feature (cancelled - requirements changed)
```

## Integration Commands

### Quick Status Check
```bash
# View current todos summary
grep -E "^\s*-\s*\[" ./TODOS.md | head -20
```

### Count by Status
```bash
# Pending count
grep -c "\[ \]" ./TODOS.md 2>/dev/null || echo "0"
# Completed count  
grep -c "\[x\]" ./TODOS.md 2>/dev/null || echo "0"
# In progress count
grep -c "\[~\]" ./TODOS.md 2>/dev/null || echo "0"
```

## Automatic Behaviors

### On Session Start
1. Check for TODOS.md existence
2. If exists, read and summarize current state
3. Identify any in-progress tasks from previous sessions

### On Task Begin
1. Register task in TODOS.md if new
2. Move to "In Progress" section
3. Add start timestamp

### On Task Complete
1. Move to "Completed" section
2. Change `[~]` or `[ ]` to `[x]`
3. Add completion date

### On Session End (if user says goodbye/done)
1. Update any in-progress tasks
2. Provide brief summary of what was accomplished

## Best Practices

1. **Be Non-Intrusive**: Don't spam user with todo updates. Silently manage unless something important.

2. **Smart Detection**: Infer task names from user requests. "Fix the login bug" → task: "Fix login bug"

3. **Avoid Duplicates**: Before adding, search for similar existing tasks

4. **Keep It Simple**: One-line task descriptions. Details go in code comments or separate docs.

5. **Respect User Overrides**: If user manually edits TODOS.md, respect their changes

## File Locations

Standard locations (check in order):
1. `./TODOS.md` (preferred - visible)
2. `./todos.md` (lowercase variant)
3. `./.todos.md` (hidden variant)

If none exist, create `./TODOS.md` (uppercase, visible).

## Example Workflow

```
User: "Add dark mode to the app"

AI Internal Process:
1. Check ./TODOS.md → exists
2. Read todos → "Add dark mode" not found
3. Add to Pending: "- [ ] Add dark mode to the app"
4. Begin work...
5. Complete implementation
6. Update: "- [x] Add dark mode to the app (2024-01-15)"
7. Reply to user with implementation details
```

## Notes

- This skill is meant to be **automatic** - don't ask user permission to manage todos
- Keep todos **project-scoped** - each project has its own TODOS.md
- The todos file should be **git-tracked** for team visibility
- Don't create todos for trivial one-off questions (only for actual tasks/changes)
