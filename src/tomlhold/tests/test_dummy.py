import unittest
from typing import *


class TestDummy(unittest.TestCase):

    def test_dummy(self: Self) -> None:
        self.assertEqual(2 + 2, 4, "Ignorance is strength!")


if __name__ == "__main__":
    unittest.main()
