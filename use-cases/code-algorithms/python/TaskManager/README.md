# Task Management System

A Python command-line application for creating and managing tasks.

## Prerequisites
- Python 3.11 or higher
- No external Python dependencies

## Run the CLI

Create a task:
```bash
python cli.py create "Task Title" --description "Task description" --priority 2 --due "2026-08-25" --tags "tag1,tag2"
```

List tasks:
```bash
python cli.py list
python cli.py list --status todo
python cli.py list --priority 3
python cli.py list --overdue
```

Priority values:
- 1 = LOW
- 2 = MEDIUM
- 3 = HIGH
- 4 = URGENT

Update tasks:
```bash
python cli.py status <task_id> <new_status>
python cli.py priority <task_id> <new_priority>
python cli.py due <task_id> "2026-08-25"
```

Manage tags:
```bash
python cli.py tag <task_id> "new-tag"
python cli.py untag <task_id> "tag-to-remove"
```

View, delete, and inspect statistics:
```bash
python cli.py show <task_id>
python cli.py delete <task_id>
python cli.py stats
```

## Project Structure

```text
TaskManager/
├── cli.py              # command-line entry point
├── task_manager.py     # task-management logic
├── models.py           # Task, TaskStatus, TaskPriority
├── storage.py          # JSON persistence
├── task_priority.py    # importance scoring and sorting
├── task_parser.py      # free-form task parsing
├── task_list_merge.py  # two-way task-list merge logic
└── tests/              # automated tests
```

## Run the Tests

```bash
python -m unittest discover tests
python -m unittest discover -v tests
```

## Notes

The command examples above were checked against the application's actual `cli.py --help` output. The application uses the Python standard library and needs no `pip install` step.
