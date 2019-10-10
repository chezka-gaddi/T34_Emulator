"""
.. module:: TestEmulator
"""
import unittest
from .Emulator import Emulator


class TestEmulator(unittest.TestCase):
    """Unit testing class for all the functionality of the Emulator class."""

    def setUp(self):
        """Setup the Emulator object to be used for all the tests."""
        self.emulator = Emulator("test.txt")

    def test_access_memory(self):
        """Test access to a memory address."""
        output = self.emulator.access_memory("200")
        self.assertEqual(output, "200\tA9")

    def test_access_memory_range(self):
        """Test access to a memory address range."""
        output = self.emulator.access_memory_range("200", "20F")
        self.assertEqual(
            output, "200\tA9 00 85 00 A5 00 8D 00\n208\t80 E6 00 4C 04 02 00 00\n")

    def test_edit_memory_locations(self):
        """Test edit of a memory location."""
        self.emulator.edit_memory(
            "300", "A9 04 85 07 A0 00 84 06 A9 A0 91 06 C8 D0 FB E6 07")
        output = self.emulator.access_memory_range("300", "310")

        self.assertEqual(
            output, "300\tA9 04 85 07 A0 00 84 06\n308\tA9 A0 91 06 C8 D0 FB E6\n310\t07\n")

    def test_run_program(self):
        """Test running the program command."""
        output = self.emulator.run_program("200")
        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n200")


if __name__ == '__main__':
    unittest.main()
