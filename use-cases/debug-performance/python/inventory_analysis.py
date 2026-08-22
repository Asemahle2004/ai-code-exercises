# inventory_analysis.py
def find_product_combinations(products, target_price, price_margin=10):
    """Find unique product pairs whose combined price is near the target."""
    results = []
    lower = target_price - price_margin
    upper = target_price + price_margin

    # Only inspect each unordered pair once: (i, j) where j > i.
    for i in range(len(products)):
        if i % 100 == 0:
            print(f"Processing product {i+1} of {len(products)}")

        product1 = products[i]
        for j in range(i + 1, len(products)):
            product2 = products[j]
            combined_price = product1["price"] + product2["price"]

            if lower <= combined_price <= upper:
                results.append({
                    "product1": product1,
                    "product2": product2,
                    "combined_price": combined_price,
                    "price_difference": abs(target_price - combined_price),
                })

    results.sort(key=lambda item: item["price_difference"])
    return results


if __name__ == "__main__":
    import random
    import time

    print("Generating Product List")
    product_list = [
        {
            "id": i,
            "name": f"Product {i}",
            "price": random.randint(5, 500),
        }
        for i in range(5000)
    ]

    print(f"Finding product combinations for {len(product_list)} products")
    start_time = time.time()
    combinations = find_product_combinations(product_list, 500, 50)
    end_time = time.time()

    print(f"Found {len(combinations)} product combinations")
    print(f"Execution time: {end_time - start_time:.2f} seconds")
