"""
.. module:: TestInstructionsIntegration
"""
import unittest
import t34
from t34.Emulator import Emulator


class TestInstructionsIntegration(unittest.TestCase):
    """Unit testing class for the integration of instructions in the Instructions class."""

    maxDiff = None

    def setUp(self):
        self.emulator = Emulator()

    # @unittest.skip
    def test_indirect_relative_absolute(self):
        """Testing indirect, relative, and absolute instructions."""
        self.emulator.edit_memory("300", "AD 09 03 6D 13 03 D0 02 00 05 6C 16 03 20 14 03 00 90 FA 05 60 00 11 03")

        output = self.emulator.run_program("300")
        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  AD  LDA    abs 09 03  05 00 00 FF 00100000\n" +
            " 303  6D  ADC    abs 13 03  0A 00 00 FF 00100000\n" +
            " 306  D0  BNE    rel 02 --  0A 00 00 FF 00100000\n" +
            " 30A  6C  JMP    ind 16 03  0A 00 00 FF 00100000\n" +
            " 311  90  BCC    rel FA --  0A 00 00 FF 00100000\n" +
            " 30D  20  JSR    abs 14 03  0A 00 00 FD 00100000\n" +
            " 314  60  RTS   impl -- --  0A 00 00 FF 00100000\n" +
            " 310  00  BRK   impl -- --  0A 00 00 FC 00110100\n")
        