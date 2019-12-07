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
        out = int(self.memory.registers[0:2].hex(), 16)
        self.assertEqual(out, 20)

    def test_get_pc(self):
        """Test retrieving address from PC register."""
        value = 20
        self.memory.registers[0:2] = value.to_bytes(2, byteorder='big')
        self.assertEqual(self.memory.get_PC(), value)

    def test_write_ac(self):
        """Test writing to AC register."""
        self.memory.write_AC(20)
        out = int(self.memory.registers[2:3].hex(), 16)
        self.assertEqual(out, 20)

    def test_get_ac(self):
        """Test retrieving address from AC register."""
        value = 20
        self.memory.registers[2:3] = value.to_bytes(1, byteorder='big')
        self.assertEqual(self.memory.get_AC(), value)

    def test_write_x(self):
        """Test writing to X register."""
        self.memory.write_X(20)
        out = int(self.memory.registers[3:4].hex(), 16)
        self.assertEqual(out, 20)

    def test_get_x(self):
        """Test retrieving address from X register."""
        value = 20
        self.memory.registers[3:4] = value.to_bytes(1, byteorder='big')
        self.assertEqual(self.memory.get_X(), value)

    def test_write_y(self):
        """Test writing to Y register."""
        self.memory.write_Y(20)
        out = int(self.memory.registers[4:5].hex(), 16)
        self.assertEqual(out, 20)

    def test_get_y(self):
        """Test retrieving address from Y register."""
        value = 20
        self.memory.registers[4:5] = value.to_bytes(1, byteorder='big')
        self.assertEqual(self.memory.get_Y(), value)

    def test_write_sp(self):
        """Test writing to SP register."""
        self.memory.write_SP(20)
        out = int(self.memory.registers[5:6].hex(), 16)
        self.assertEqual(out, 20)

    def test_get_sp(self):
        """Test retrieving address from Y register."""
        value = 20
        self.memory.registers[5:6] = value.to_bytes(1, byteorder='big')
        self.assertEqual(self.memory.get_SP(), value)

    def test_write_sr(self):
        """Test writing to SR register."""
        self.memory.write_SR(20)
        out = int(self.memory.registers[6:7].hex(), 16)
        self.assertEqual(out, 20)

    def test_get_sr(self):
        """Test retrieving address from Y register."""
        value = 20
        self.memory.registers[6:7] = value.to_bytes(1, byteorder='big')
        self.assertEqual(self.memory.get_SR(), value)


if __name__ == '__main__':
    unittest.main()
