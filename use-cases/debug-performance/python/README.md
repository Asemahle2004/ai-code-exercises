# Inventory Analyzer - Performance Optimization Challenge

A Python tool for analyzing product inventory to find combinations of products that match specific price targets.

## Features

- Find pairs of products whose combined price matches a target price within a specified margin
- Handles large product inventories efficiently
- Progress tracking for long-running analyses
- Sorted results by closest match to target price
- Duplicate combination prevention by considering each unordered pair once

## Usage

The main function `find_product_combinations` takes the following parameters:

```python
def find_product_combinations(products, target_price, price_margin=10):
    """
    Args:
        products: List of dictionaries with 'id', 'name', and 'price' keys
        target_price: The ideal combined price
        price_margin: Acceptable deviation from the target price
    """
```

### Example Usage

```python
product_list = [
    {'id': 1, 'name': 'Product 1', 'price': 100},
    {'id': 2, 'name': 'Product 2', 'price': 200},
]

combinations = find_product_combinations(product_list, 300, 0)
```

Each result contains:
- Product 1 details
- Product 2 details
- Combined price
- Price difference from target

## How to run

Run the full 5,000-product demonstration:

```bash
python inventory_analysis.py
```

Run the deterministic regression tests:

```bash
python -m unittest -v test_inventory_analysis.py
```

The tests check that an exact target pair is returned once, that a product is not paired with itself, and that results remain sorted by closeness to the target price.

## Performance and verification

The optimized loop starts the second index at `i + 1`, so `(A, B)` is evaluated but `(B, A)` is not evaluated again. This removes the need to scan the growing results list to eliminate reversed duplicates.

A Windows verification run on 5,000 generated products completed successfully and returned 2,431,319 qualifying combinations in 9.56 seconds. Because the generated product prices are random, the combination count and timing can differ between runs and computers. The deterministic unit tests should be used for repeatable correctness checks.
