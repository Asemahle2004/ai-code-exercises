# Local Verification Record

This file records verification runs performed on the Windows clone after the exercise changes were pulled from the fork.

## Code comprehension Task Manager

Command:

```powershell
python -m unittest discover -v tests
```

Result:

```text
Ran 31 tests in 0.109s
OK
```

The CLI was also inspected with `python cli.py --help`, and a real task was created, listed, and inspected in `tasks.json` to trace the flow from the CLI through storage.

## Error Diagnosis Challenge

Command:

```powershell
python -m unittest discover -v tests
```

Result from the supplied test suite after the off-by-one fix:

```text
Ran 2 tests in 0.021s
OK
```

A later follow-up commit adds an empty-inventory regression test as additional edge-case coverage. That new test should be run again after pulling the latest repository changes.

## Performance Optimization Challenge

A deterministic three-product check used prices 100, 200, and 300 with a target of 300 and margin of 0. It returned only the 100 + 200 pair once, confirming that the optimized loop does not return the reversed duplicate.

A full demonstration run then processed 5,000 generated products:

```text
Found 2431319 product combinations
Execution time: 9.56 seconds
```

Because the product prices are randomly generated, the result count and timing can differ between runs. A separate deterministic unit-test file was added afterward so correctness can be checked repeatably without relying on random data.

## Testing With AI

Command:

```powershell
python -m unittest discover -v tests
```

Result:

```text
Ran 6 tests in 0.005s
OK
```

These tests cover task-priority scoring, status and due-date effects, important-tag behaviour, ordering, and top-N limiting.

## Function Decomposition Challenge

Command:

```powershell
python -m unittest -v test_sales_report.py
```

Result:

```text
Ran 8 tests in 0.046s
OK
```

This confirmed that the refactored `generate_sales_report()` structure still preserved the behaviours checked by the supplied tests.

## AI Solution Verification Challenge

Command:

```powershell
node test_merge_sort.js
```

Result:

```text
Running merge_sort tests...
All tests completed
```

The corrected leftover-left loop increments `i`, allowing the merge to make progress instead of getting stuck.

## Repository synchronization check

At the end of the verification session, `git status` reported a clean working tree and the local `HEAD` matched `origin/main` at that point in time. New follow-up documentation and regression-test commits were added afterward, so the Windows clone needs another `git pull` before the next local verification run.
