# test_stock_manager.py
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from stock_manager import main, print_inventory_report


class TestStockManager(unittest.TestCase):
    def test_print_inventory_report(self):
        items = [
            {"name": "Test Item 1", "quantity": 10},
            {"name": "Test Item 2", "quantity": 20},
        ]

        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            print_inventory_report(items)

        result = captured_output.getvalue()
        self.assertIn("Item 1: Test Item 1 - Quantity: 10", result)
        self.assertIn("Item 2: Test Item 2 - Quantity: 20", result)

    def test_empty_inventory_prints_report_without_crashing(self):
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            print_inventory_report([])

        result = captured_output.getvalue()
        self.assertIn("===== INVENTORY REPORT =====", result)
        self.assertIn("============================", result)
        self.assertNotIn("Item 1:", result)

    def test_main_function(self):
        with patch("stock_manager.print_inventory_report") as mock_print:
            main()

        self.assertEqual(mock_print.call_count, 1)
        args, _ = mock_print.call_args
        items = args[0]
        self.assertEqual(len(items), 3)
        self.assertEqual(items[0]["name"], "Laptop")
        self.assertEqual(items[1]["quantity"], 30)


if __name__ == "__main__":
    unittest.main()
