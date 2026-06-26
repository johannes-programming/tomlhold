"""Run the unit tests for the tomlhold package."""

from __future__ import annotations

__all__: list[str] = ["main"]

import unittest


def main() -> unittest.TextTestResult:
    "Run discovered tests via unittest and return the TextTestResult."
    loader: unittest.TestLoader
    suite: unittest.TestSuite
    runner: unittest.TextTestRunner
    loader = unittest.TestLoader()
    suite = loader.discover("tests")
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == "__main__":
    main()
