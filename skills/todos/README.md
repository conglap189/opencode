# Todos Skill

Automatic todo tracking and task management for projects.

## Features

- **Auto-detection**: Automatically checks for TODOS.md in project root
- **Auto-creation**: Creates TODOS.md if it doesn't exist
- **Task tracking**: Tracks pending, in-progress, and completed tasks
- **Smart updates**: Automatically updates task status as work progresses

## Usage

This skill activates automatically when the AI starts working on any task. No explicit activation needed.

### Manual Activation

If needed, you can explicitly load the skill:
```
/skill todos
```

Or ask the AI to check todos:
```
Check the project todos
What tasks are pending?
Mark [task] as complete
```

## File Format

The skill uses a standard Markdown format with checkboxes:

```markdown
## Pending
- [ ] Task not started
- [~] Task in progress
- [!] Task blocked

## Completed
- [x] Completed task (2024-01-15)
- [-] Cancelled task
```

## Integration

The skill integrates with the AI workflow to:
1. Check todos at session start
2. Register new tasks when work begins
3. Update status when tasks complete
4. Provide summaries on request

## Configuration

No configuration needed. The skill uses sensible defaults:
- File location: `./TODOS.md` in project root
- Format: Standard Markdown with checkboxes
- Git-friendly: Designed to be version controlled
