import datetime
import unittest

from tomlhold.core import Holder 


class TestHolderDataTypes(unittest.TestCase):

    def setUp(self):
        """
        This method is called before each test case to set up a new instance of the Holder class.
        """
        self.holder = Holder()

    def test_string(self):
        """Test if strings are stored and retrieved correctly."""
        self.holder["string_key"] = "Hello, World!"
        self.assertEqual(self.holder["string_key"], "Hello, World!")

    def test_integer(self):
        """Test if integers are stored and retrieved correctly."""
        self.holder["integer_key"] = 42
        self.assertEqual(self.holder["integer_key"], 42)

    def test_float(self):
        """Test if floats are stored and retrieved correctly."""
        self.holder["float_key"] = 3.14159
        self.assertEqual(self.holder["float_key"], 3.14159)

    def test_boolean(self):
        """Test if booleans are stored and retrieved correctly."""
        self.holder["boolean_key_true"] = True
        self.holder["boolean_key_false"] = False
        self.assertTrue(self.holder["boolean_key_true"])
        self.assertFalse(self.holder["boolean_key_false"])

    def test_array(self):
        """Test if arrays (lists) are stored and retrieved correctly."""
        array_data = [1, 2, 3, "four", True]
        self.holder["array_key"] = array_data
        self.assertListEqual(self.holder["array_key"], array_data)

    def test_datetime(self):
        """Test if datetimes are stored and retrieved correctly."""
        datetime_value = datetime.datetime(2023, 10, 22, 14, 45, 0)
        self.holder["datetime_key"] = datetime_value
        self.assertEqual(self.holder["datetime_key"], datetime_value)

    def test_date(self):
        """Test if dates are stored and retrieved correctly."""
        date_value = datetime.date(2023, 10, 22)
        self.holder["date_key"] = date_value
        self.assertEqual(self.holder["date_key"], date_value)

    def test_time(self):
        """Test if times are stored and retrieved correctly."""
        time_value = datetime.time(14, 45, 0)
        self.holder["time_key"] = time_value
        self.assertEqual(self.holder["time_key"], time_value)

    def test_nested_tables(self):
        """Test if nested tables (dictionaries) are stored and retrieved correctly."""
        nested_data = {
            "key1": "value1",
            "key2": {
                "nested_key1": "nested_value1",
                "nested_key2": {"deep_key": "deep_value"},
            },
        }
        self.holder["nested_table"] = nested_data
        self.assertEqual(self.holder["nested_table"]["key1"], "value1")
        self.assertEqual(
            self.holder["nested_table", "key2", "nested_key1"], "nested_value1"
        )
        self.assertEqual(
            self.holder["nested_table"]["key2"]["nested_key2"]["deep_key"], "deep_value"
        )

    def test_mixed_array(self):
        """Test if mixed-type arrays are stored and retrieved correctly."""
        mixed_array = [1, "two", 3.0, True, {"nested_key": "nested_value"}]
        self.holder["mixed_array_key"] = mixed_array
        self.assertEqual(self.holder["mixed_array_key"], mixed_array)

    def test_multiline_string(self):
        """Test if multiline strings are stored and retrieved correctly."""
        multiline_string = """This is a
multiline string
with several lines."""
        self.holder["multiline_string_key"] = multiline_string
        self.assertEqual(self.holder["multiline_string_key"], multiline_string)

    def test_empty_table(self):
        """Test if empty tables (dictionaries) are handled correctly."""
        self.holder["empty_table"] = {}
        self.assertEqual(self.holder["empty_table"], {})

    def test_update_with_multiple_data_types(self):
        """Test updating the Holder with multiple data types at once."""
        update_data = {
            "string": "test_string",
            "integer": 100,
            "float": 9.81,
            "boolean": False,
            "datetime": datetime.datetime(2023, 1, 1, 0, 0, 0),
            "array": [1, 2, 3],
        }
        self.holder.update(update_data)
        self.assertEqual(self.holder["string"], "test_string")
        self.assertEqual(self.holder["integer"], 100)
        self.assertEqual(self.holder["float"], 9.81)
        self.assertFalse(self.holder["boolean"])
        self.assertEqual(
            self.holder["datetime"], datetime.datetime(2023, 1, 1, 0, 0, 0)
        )
        self.assertListEqual(self.holder["array"], [1, 2, 3])

    def test_holder_as_toml_string(self):
        """Test if Holder can be serialized back into TOML format correctly."""
        toml_data = """
        key1 = "value1"
        key2 = 42
        float_key = 3.14
        boolean_key = true
        array_key = [1, 2, 3, "four"]
        """
        holder = Holder.loads(toml_data)
        toml_string = holder.dumps()
        self.assertIn('key1 = "value1"', toml_string)
        self.assertIn("key2 = 42", toml_string)
        self.assertIn("float_key = 3.14", toml_string)
        self.assertIn("boolean_key = true", toml_string)


if __name__ == "__main__":
    unittest.main()
