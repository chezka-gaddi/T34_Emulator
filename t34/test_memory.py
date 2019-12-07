"""
.. module:: TestMemory
"""
import unittest
from .Memory import Memory


class TestMemory(unittest.TestCase):
    """Unit testing class for all the functionality of the Emulator class."""

    def setUp(self):
        """Setup the Emulator object to be used for all the tests."""
        self.memory = Memory()

    def test_write_pc(self):
        """Test writing to PC register."""
        self.memory.write_PC(20)
        pc = int(self.memory.registers[0:2].hex(), 16)
        self.assertEqual(pc, 20)

    def test_get_pc(self):
        """Test retrieving address from PC register."""
        value = 20
        self.memory.registers[0:2] = value.to_bytes(2, byteorder='big')
        self.assertEqual(self.memory.get_PC(), value)

    def test_write_ac(self):
        """Test writing to AC register."""
        self.memory.write_AC(20)
        pc = int(self.memory.registers[2:3].hex(), 16)
        self.assertEqual(pc, 20)

    def test_get_ac(self):
        """Test retrieving address from AC register."""
        value = 20
        self.memory.registers[2:3] = value.to_bytes(1, byteorder='big')
        self.assertEqual(self.memory.get_AC(), value)


if __name__ == '__main__':
    unittest.main()
