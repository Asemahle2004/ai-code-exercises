# Task Management System

## Usage Instructions

### Prerequisites
- Python 3.11 or higher
- No additional external dependencies required

### Installation
1. Clone your fork of the repository.
2. Open a terminal in this `TaskManager` folder.
3. No package installation is required because the project uses the Python standard library.

### Run the CLI

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

Update a task:
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

### Run the Tests

Run all tests in the exercise:
```bash
python -m unittest discover -v tests
```

The added tests focus on task-priority scoring, status and tag adjustments, ordering by importance, and limiting the returned top-priority tasks.
