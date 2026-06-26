"""Test the TOMLDict class."""

from __future__ import annotations

__all__: list[str] = ["TestTOMLDict"]
import io
import math
import os
import tempfile
import unittest
from datetime import date, datetime, time, timezone
from typing import Any

from tomlhold import TOMLDict, TOMLList


class TestTOMLDict(unittest.TestCase):
    "Test the TOMLDict class and its TOML data handling behavior."

    def test_keys_are_converted_to_strings(self) -> None:
        "Test that keys are converted to strings."
        holder: TOMLDict
        holder = TOMLDict({1: "one", "two": 2})  # type: ignore[arg-type]

        self.assertIn("1", holder.data)
        self.assertNotIn(1, holder.data)
        self.assertEqual(holder.data["1"], "one")
        self.assertEqual(holder.data["two"], 2)

    def test_nested_mappings_and_sequences_are_wrapped(self) -> None:
        "Test that nested mappings and sequences are wrapped in holders."
        holder: TOMLDict
        holder = TOMLDict(
            {
                "table": {"answer": 42},
                "array": ["a", "b", {"nested": True}],
                "string": "abc",
            }
        )

        self.assertIsInstance(holder.data["table"], TOMLDict)
        self.assertEqual(holder.data["table"].data["answer"], 42)

        self.assertIsInstance(holder.data["array"], TOMLList)
        self.assertEqual(holder.data["array"].data[0], "a")
        self.assertEqual(holder.data["array"].data[1], "b")
        self.assertIsInstance(holder.data["array"].data[2], TOMLDict)
        self.assertIs(holder.data["array"].data[2].data["nested"], True)

        # Strings are sequences in Python, but should remain strings.
        self.assertEqual(holder.data["string"], "abc")

    def test_supported_scalar_values_are_preserved(self) -> None:
        "Test that supported scalar values are preserved."
        dt: datetime
        d: date
        t: time
        holder: TOMLDict
        dt = datetime(2026, 6, 13, 12, 30, 15, 123456, tzinfo=timezone.utc)
        d = date(2026, 6, 13)
        t = time(12, 30, 15, 123456, tzinfo=timezone.utc)

        holder = TOMLDict(
            {
                "string": "value",
                "bool": True,
                "int": 123,
                "float": 1.5,
                "datetime": dt,
                "date": d,
                "time": t,
                "none": None,
            }
        )

        self.assertEqual(holder.data["string"], "value")
        self.assertIs(holder.data["bool"], True)
        self.assertEqual(holder.data["int"], 123)
        self.assertEqual(holder.data["float"], 1.5)
        self.assertEqual(holder.data["datetime"], dt)
        self.assertEqual(holder.data["date"], d)
        self.assertEqual(holder.data["time"], t)
        self.assertTrue(math.isnan(holder.data["none"]))

    def test_invalid_value_type_raises_type_error(self) -> None:
        "Test that invalid value type raises type error."

        class Unsupported:
            "Unsupported dummy class used to test type validation error."

        with self.assertRaises(TypeError):
            TOMLDict({"bad": Unsupported()})

    def test_data_assignment_rebuilds_holder_data(self) -> None:
        "Test that data assignment rebuilds holder data."
        holder: TOMLDict
        holder = TOMLDict({"old": 1})
        holder.data = {"new": [1, 2, 3]}
        self.assertNotIn("old", holder.data)
        self.assertIn("new", holder.data)
        self.assertIsInstance(holder.data["new"], TOMLList)
        self.assertEqual(holder.data["new"].data, (1, 2, 3))

    def test_dumps_and_loads_round_trip(self) -> None:
        "Test dumps and loads round trip."
        original: TOMLDict
        dumped: str
        loaded: TOMLDict
        original = TOMLDict(
            {
                "project": {"name": "tomlhold", "version": "2.0.0"},
                "numbers": [1, 2, 3],
                "enabled": True,
            }
        )

        dumped = original.dumps()
        loaded = TOMLDict.loads(dumped)

        self.assertIsInstance(dumped, str)
        self.assertEqual(loaded.data["project"].data["name"], "tomlhold")
        self.assertEqual(loaded.data["project"].data["version"], "2.0.0")
        self.assertEqual(loaded.data["numbers"].data, (1, 2, 3))
        self.assertIs(loaded.data["enabled"], True)

    def test_dump_and_load_byte_stream_round_trip(self) -> None:
        "Test dump and load byte stream round trip."
        loaded: TOMLDict
        original: TOMLDict
        stream: io.BytesIO
        original = TOMLDict({"name": "stream", "values": [1, 2]})
        stream = io.BytesIO()
        original.dump(stream)
        stream.seek(0)
        loaded = TOMLDict.load(stream)
        self.assertEqual(loaded.data["name"], "stream")
        self.assertEqual(loaded.data["values"].data, (1, 2))

    def test_dumpintofile_and_loadfromfile_round_trip(self) -> None:
        "Test dumpintofile and loadfromfile round trip."
        loaded: TOMLDict
        original: TOMLDict
        tmpdir: str
        path: str
        original = TOMLDict({"name": "file", "values": [3, 4]})

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.toml")
            original.dumpintofile(path)
            loaded = TOMLDict.loadfromfile(path)

        self.assertEqual(loaded.data["name"], "file")
        self.assertEqual(loaded.data["values"].data, (3, 4))


if __name__ == "__main__":
    unittest.main()
