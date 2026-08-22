# WeThinkCode_ AI Code Exercises — Submission Record

This file documents the work completed for the exercises listed in the repository README. The exercises were completed primarily with the Python starter code, except for the AI Solution Verification Challenge, whose supplied starter is JavaScript.

## 1. Code Exploration Challenge

### Project explored
`use-cases/code-comprehension-001/python/TaskManager`

### Mental model
The application is a command-line Task Manager with separated responsibilities:

```text
User command
    ↓
cli.py
    ↓
task_manager.py
    ↓
models.py + storage.py
    ↓
tasks.json
```

- `cli.py` parses terminal commands and calls the appropriate manager method.
- `task_manager.py` contains task-management/business logic.
- `models.py` defines task state, priority, and the Task object.
- `storage.py` loads and persists tasks as JSON.

### Verification performed
The CLI was inspected with `python cli.py --help`. The Python unit-test suite was then run with `python -m unittest discover -v tests`; 31 tests passed. A real task was created, listed, and inspected in `tasks.json` to verify the data flow from command input to persisted JSON.

### Key learning
When entering an unfamiliar codebase, first identify the entry point and major components, then trace one concrete feature through those components instead of trying to read every file at once.

---

## 2. Algorithm Deconstruction Challenge

### Algorithm selected
Task priority scoring and sorting in:
`use-cases/code-algorithms/python/TaskManager/task_priority.py`

### Step-by-step understanding
1. Map each priority level to a weight.
2. Multiply the weight by 10 to form the base score.
3. Add a due-date bonus when a task is overdue or due soon.
4. Subtract points for DONE or REVIEW status.
5. Add one important-tag bonus when a task contains `blocker`, `critical`, or `urgent`.
6. Add a recent-update bonus.
7. Sort tasks by the calculated score from highest to lowest.
8. Slice the sorted list when only the top N tasks are required.

### Example
A HIGH-priority, overdue task with a `critical` tag and a recent update receives:

```text
HIGH base       40
Overdue bonus  +35
Important tag   +8
Recent update   +5
------------------
Total           88
```

### Reflection
The important idea is that priority is not just one label. Several task attributes are converted into one comparable score. A useful improvement would be to move the scoring constants into named constants or configuration so the business rules are easier to adjust and understand.

---

## 3. Knowing Where to Start

### Initial project map
For the Python Task Manager, the practical starting sequence is:

1. Read `README.md` to identify the application purpose and run commands.
2. Inspect `cli.py` because it is the command-line entry point.
3. Follow imports and method calls into `task_manager.py`.
4. Inspect `models.py` to understand the domain objects and enums.
5. Inspect `storage.py` to understand persistence.
6. Look at `tests/` to see expected behaviour.
7. Run the program and tests to verify assumptions.

### Technology stack
- Python 3.11+
- Python standard library
- `argparse` for CLI parsing
- `json` for persistence
- `unittest` for automated tests

### Verification insight
The actual `cli.py --help` output was compared with the README. This exposed a documentation mismatch in some update/tag command names, demonstrating why code and runtime behaviour should be checked instead of relying on documentation alone.

---

## 4. Code Documentation

### Function documented
`calculate_task_score(task)` in the Python Task Manager.

### Verified documentation
The function calculates a numerical importance score from these rules:

- LOW = 10 base points
- MEDIUM = 20 base points
- HIGH = 40 base points
- URGENT = 60 base points
- overdue = +35
- due today = +20
- due within 2 days = +15
- due within 7 days = +10
- DONE = -50
- REVIEW = -15
- at least one important tag = +8
- updated less than one day ago = +5

The important-tag bonus is applied once even when multiple important tags are present. The result can be negative and depends on the current time because `datetime.now()` is used.

### Documentation lesson
AI-generated documentation should be treated as a draft. Parameters, scoring rules, examples, edge cases, and runtime assumptions must be checked against the source code.

---

## 5. README Documentation

### Documentation review
The Task Manager README was checked against the actual CLI implementation. The testing exercise README was updated so that its command examples match the program's real commands:

```text
status
priority
due
tag
untag
show
delete
stats
```

It now also documents how to run the added unit tests:

```bash
python -m unittest discover -v tests
```

### Key learning
A README is useful only when it reflects the program users actually run. Runtime help such as `python cli.py --help` is a valuable source for verifying command documentation.

---

## 6. Error Diagnosis Challenge

### Selected bug
Python off-by-one error in:
`use-cases/debug-errors-001/python/stock_manager.py`

### Root cause
The original loop used:

```python
for i in range(len(items) + 1):
```

For a list of length 3, that produces indexes 0, 1, 2, and 3, but index 3 does not exist. The symptom is `IndexError: list index out of range`.

### Fix implemented
The loop now uses:

```python
for i in range(len(items)):
```

This iterates over exactly the valid indexes.

### Key learning
The traceback identifies where the invalid access occurred, while debugging must still identify the earlier logic that produced the invalid index.

---

## 7. Performance Optimization Challenge

### Selected code
`use-cases/debug-performance/python/inventory_analysis.py`

### Bottleneck identified
The original implementation:

- compared every product with every other product,
- evaluated both `(A, B)` and `(B, A)`, and
- repeatedly scanned the growing result list with `any(...)` to remove duplicates.

### Optimization implemented
The inner loop now starts at `i + 1`:

```python
for i in range(len(products)):
    for j in range(i + 1, len(products)):
```

Each unordered pair is therefore considered once, so the expensive duplicate-result scan is no longer needed.

### Verification benchmark
A local synthetic benchmark using 250 products produced the same 6,133 qualifying unordered pairs before and after optimization. In that check, the original implementation took about 1.75 seconds and the optimized implementation about 0.006 seconds. Exact timings vary by computer and dataset; the important result is that correctness was preserved while the unnecessary duplicate work was removed.

---

## 8. AI Solution Verification Challenge

### Selected starter
`use-cases/debug-limitations/javascript/merge_sort.js`

### AI suggestion checked
The broken leftover-left loop incremented `j` instead of `i`:

```javascript
while (i < left.length) {
    result.push(left[i]);
    j++;
}
```

That can prevent `i` from advancing and cause the loop to get stuck.

### Fix implemented

```javascript
while (i < left.length) {
    result.push(left[i]);
    i++;
}
```

### Verification
The corrected merge-sort logic was checked with six Node assertion scenarios: empty array, one element, already sorted input, reverse-sorted input, duplicates, and a larger array. All six verification cases passed.

### Key learning
A plausible AI fix is still only a hypothesis until the exact code path is checked and tested. Small targeted tests make that verification explicit.

---

## 9. Using AI to Help With Testing

### Code selected
Task-priority behaviour in:
`use-cases/testing-001/python/TaskManager/task_priority.py`

### Tests added
`tests/test_task_priority.py` now checks:

- medium-priority base score plus recent-update bonus,
- important-tag bonus being applied once,
- DONE status reducing a score,
- due-within-a-week bonus,
- descending importance ordering, and
- the top-priority result limit.

The test design focuses on observable behaviour rather than implementation details. The test cases were first validated locally against the supplied Task and priority-scoring code; all six passed.

### Key learning
AI is most useful for helping identify behaviours and edge cases. The developer should still understand each assertion and be able to explain why the expected result is correct.

---

## 10. Function Decomposition Challenge

### Selected function
`generate_sales_report()` in:
`use-cases/refactor-functions/python/sales_report.py`

### Problem
The original function handled many responsibilities at once: validation, date filtering, field filtering, metrics, grouping, detailed calculations, forecasting, charts, and output selection.

### Refactoring implemented
The work was separated into focused helpers including:

- `validate_report_parameters()`
- `filter_sales_by_date_range()`
- `apply_sales_filters()`
- `calculate_sales_metrics()`
- `group_sales_data()`
- `build_detailed_transactions()`
- `calculate_sales_forecast()`
- `generate_chart_data()`
- `handle_empty_report()`
- `generate_report_output()`

The main `generate_sales_report()` function now coordinates these smaller responsibilities.

### Verification
Before writing the refactor to the fork, the refactored logic was checked against the eight supplied Python sales-report tests; all eight passed in that validation run.

### Benefits
The decomposition makes individual responsibilities easier to read, test, debug, reuse, and modify without having to reason through one very large function.

---

## Final Submission Note

The repository contains the starter code plus the implemented debugging, performance, verification, testing, and refactoring changes described above. This document provides the written analysis and reflections for the exercises whose main deliverable is understanding or documentation.
