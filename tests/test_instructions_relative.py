"""
.. module:: TestInstructionsRelative
"""
import unittest
import t34
from t34.Emulator import Emulator


class TestInstructionsRelative(unittest.TestCase):
    """Unit testing class for all relative addressed instructions in the Instructions class."""

    maxDiff = None

    def setUp(self):
        self.emulator = Emulator()

    def test_jmp_ind(self):
        """Test jmp ind instruction."""
        self.emulator.edit_memory("300", "6C 0A 03 00 00 00")
        self.emulator.edit_memory("30A", "05 03")

        output = self.emulator.run_program("300")
        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  6C  JMP    ind 0A 03  00 00 00 FF 00100000\n" +
            " 305  00  BRK   impl -- --  00 00 00 FC 00110100\n")

    def test_bcc_rel(self):
        """Test bcc rel instruction."""
        self.emulator.edit_memory("300", "90 05 00")
        self.emulator.edit_memory("305", "00")

        output = self.emulator.run_program("300")
        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  90  BCC    rel 05 --  00 00 00 FF 00100000\n" +
            " 305  00  BRK   impl -- --  00 00 00 FC 00110100\n")

    def test_bcs_rel(self):
        """Test bcs rel instruction."""
        self.emulator.set_carry()
        self.emulator.edit_memory("300", "B0 05 00")
        self.emulator.edit_memory("305", "00")

        output = self.emulator.run_program("300")
        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  B0  BCS    rel 05 --  00 00 00 FF 00100001\n" +
            " 305  00  BRK   impl -- --  00 00 00 FC 00110101\n")

    def test_beq_rel(self):
        """Test beq rel instruction."""
        self.emulator.set_zero()
        self.emulator.edit_memory("300", "F0 05 00")
        self.emulator.edit_memory("305", "00")

        output = self.emulator.run_program("300")
        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  F0  BEQ    rel 05 --  00 00 00 FF 00100010\n" +
            " 305  00  BRK   impl -- --  00 00 00 FC 00110110\n")

    def test_bmi_rel(self):
        """Test bmi rel instruction."""
        self.emulator.set_zero()
        self.emulator.set_negative()
        self.emulator.edit_memory("300", "30 05 00")
        self.emulator.edit_memory("305", "00")

        output = self.emulator.run_program("300")
        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  30  BMI    rel 05 --  00 00 00 FF 10100010\n" +
            " 305  00  BRK   impl -- --  00 00 00 FC 10110110\n")

    def test_bne_rel(self):
        """Test bne rel instruction."""
        self.emulator.edit_memory("300", "D0 05 00")
        self.emulator.edit_memory("305", "00")

        output = self.emulator.run_program("300")
        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  D0  BNE    rel 05 --  00 00 00 FF 00100000\n" +
            " 305  00  BRK   impl -- --  00 00 00 FC 00110100\n")

    def test_bpl_rel(self):
        """Test bpl rel instruction."""
        self.emulator.edit_memory("300", "10 05 00")
        self.emulator.edit_memory("305", "00")

        output = self.emulator.run_program("300")
        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  10  BPL    rel 05 --  00 00 00 FF 00100000\n" +
            " 305  00  BRK   impl -- --  00 00 00 FC 00110100\n")

    def test_bvc(self):
        """Test bvc instruction."""
        self.emulator.edit_memory("300", "50 05 00")
        self.emulator.edit_memory("305", "00")

        output = self.emulator.run_program("300")
        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  50  BVC    rel 05 --  00 00 00 FF 00100000\n" +
            " 305  00  BRK   impl -- --  00 00 00 FC 00110100\n")

    def test_bvs(self):
        """Test bvs instruction."""
        self.emulator.set_overflow()
        self.emulator.edit_memory("300", "70 05 00")
        self.emulator.edit_memory("305", "00")

        output = self.emulator.run_program("300")
        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  70  BVS    rel 05 --  00 00 00 FF 01100000\n" +
            " 305  00  BRK   impl -- --  00 00 00 FC 01110100\n")
