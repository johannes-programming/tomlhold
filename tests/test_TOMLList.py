from __future__ import annotations

import unittest

from tomlhold import TOMLDict, TOMLList

__all__ = ["TestTOMLList"]


class TestTOMLList(unittest.TestCase):
    def test_list_data_is_stored_as_tuple(self) -> None:
        holder = TOMLList([1, "two", True])

        self.assertEqual(holder.data, (1, "two", True))
        self.assertIsInstance(holder.data, tuple)

    def test_nested_values_are_wrapped(self) -> None:
        holder = TOMLList([{"name": "item"}, [1, 2], "abc"])

        self.assertIsInstance(holder.data[0], TOMLDict)
        self.assertEqual(holder.data[0].data["name"], "item")
        self.assertIsInstance(holder.data[1], TOMLList)
        self.assertEqual(holder.data[1].data, (1, 2))
        self.assertEqual(holder.data[2], "abc")

    def test_invalid_list_value_type_raises_type_error(self) -> None:
        class Unsupported:
            pass

        with self.assertRaises(TypeError):
            TOMLList([Unsupported()])

    def test_data_assignment_rebuilds_list_data(self) -> None:
        holder = TOMLList([1])

        holder.data = [{"nested": "yes"}]

        self.assertEqual(len(holder.data), 1)
        self.assertIsInstance(holder.data[0], TOMLDict)
        self.assertEqual(holder.data[0].data["nested"], "yes")


if __name__ == "__main__":
    unittest.main()
