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

Initial supplied-test verification after the off-by-one fix:

```powershell
python -m unittest discover -v tests
```

```text
Ran 2 tests in 0.021s
OK
```

A follow-up regression test was then added for the empty-inventory edge case. After pulling that change to the Windows clone, the expanded suite was run again:

```text
Ran 3 tests in 0.172s
OK
```

The three passing tests now cover normal report output, an empty inventory, and the `main()` call path.

## Performance Optimization Challenge

A deterministic three-product check used prices 100, 200, and 300 with a target of 300 and margin of 0. It returned only the 100 + 200 pair once, confirming that the optimized loop does not return the reversed duplicate.

A full demonstration run then processed 5,000 generated products:

```text
Found 2431319 product combinations
Execution time: 9.56 seconds
```

Because the product prices are randomly generated, the result count and timing can differ between runs.

A separate deterministic regression-test file was added afterward. After pulling it to the Windows clone, it was run with:

```powershell
python -m unittest -v test_inventory_analysis.py
```

Result:

```text
Ran 3 tests in 0.004s
OK
```

Those tests verify that an exact target pair is returned only once, a single product is not paired with itself, and qualifying results remain sorted by price difference.

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

The Windows clone was pulled after the first round of follow-up improvements, and both new regression suites passed locally. This verification record was then updated on GitHub with those measured results, so the clone needs one final `git pull` before a final local `HEAD` versus `origin/main` comparison.
