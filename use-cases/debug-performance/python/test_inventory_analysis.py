import io
import unittest
from contextlib import redirect_stdout

from inventory_analysis import find_product_combinations


class TestInventoryAnalysis(unittest.TestCase):
    def run_quietly(self, products, target_price, price_margin=10):
        with redirect_stdout(io.StringIO()):
            return find_product_combinations(products, target_price, price_margin)

    def test_exact_target_pair_is_returned_once(self):
        products = [
            {"id": 1, "name": "A", "price": 100},
            {"id": 2, "name": "B", "price": 200},
            {"id": 3, "name": "C", "price": 300},
        ]

        results = self.run_quietly(products, 300, 0)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["product1"]["id"], 1)
        self.assertEqual(results[0]["product2"]["id"], 2)
        self.assertEqual(results[0]["combined_price"], 300)
        self.assertEqual(results[0]["price_difference"], 0)

    def test_single_product_is_not_paired_with_itself(self):
        products = [{"id": 1, "name": "A", "price": 150}]

        results = self.run_quietly(products, 300, 0)

        self.assertEqual(results, [])

    def test_results_are_sorted_by_closest_price(self):
        products = [
            {"id": 1, "name": "A", "price": 100},
            {"id": 2, "name": "B", "price": 195},
            {"id": 3, "name": "C", "price": 205},
            {"id": 4, "name": "D", "price": 210},
        ]

        results = self.run_quietly(products, 300, 10)
        differences = [result["price_difference"] for result in results]

        self.assertEqual(differences, sorted(differences))
        self.assertEqual(differences, [5, 5, 10])


if __name__ == "__main__":
    unittest.main()
