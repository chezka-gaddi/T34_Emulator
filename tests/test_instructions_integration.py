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

    @unittest.skip("Question about BNE")
    def test_indirect_relative_absolute(self):
        """Testing indirect, relative, and absolute instructions."""
        self.emulator.edit_memory(
            "300", "AD 09 03 6D 13 03 D0 02 00 05 6C 16 03 20 14 03 00 90 FA 05 60 00 11 03")

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

    def test_absolute(self):
        """Testing absolute instructions."""
        self.emulator.edit_memory(
            "1000", "01 03 05 07 09 0B 0D 0F 00 02 04 06 08 0A 0C 0E 10 30 50 70 90 B0 D0 F0 00 20 40 60 80 A0 C0 E0")
        self.emulator.edit_memory(
            "300", "AD 00 10 0D 13 10 8D 20 10 6D 06 10 6D 10 10 2C 20 10 0E 1D 10 6E 09 10")

        output = self.emulator.run_program("300")
        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  AD  LDA    abs 00 10  01 00 00 FF 00100000\n" +
            " 303  0D  ORA    abs 13 10  71 00 00 FF 00100000\n" +
            " 306  8D  STA    abs 20 10  71 00 00 FF 00100000\n" +
            " 309  6D  ADC    abs 06 10  7E 00 00 FF 00100000\n" +
            " 30C  6D  ADC    abs 10 10  8E 00 00 FF 11100000\n" +
            " 30F  2C  BIT    abs 20 10  8E 00 00 FF 01100010\n" +
            " 312  0E  ASL    abs 1D 10  8E 00 00 FF 01100001\n" +
            " 315  6E  ROR    abs 09 10  8E 00 00 FF 11100000\n" +
            " 318  00  BRK   impl -- --  8E 00 00 FC 11110100\n")

        output = self.emulator.access_memory_range("1000", "1027")
        self.assertEqual(
            output, "1000\t01 03 05 07 09 0B 0D 0F\n" +
            "1008\t00 81 04 06 08 0A 0C 0E\n" +
            "1010\t10 30 50 70 90 B0 D0 F0\n" +
            "1018\t00 20 40 60 80 40 C0 E0\n" +
            "1020\t71 00 00 00 00 00 00 00\n")

    @unittest.skip("Infinite Loop")
    def test_indirect_relative_absolute_infinite(self):
        self.emulator.edit_memory(
            "300", "A9 01 85 00 18 2A A5 00 8D 00 80 A2 03 A0 03 88 D0 FD CA D0 F8 4C 05 03")

        output = self.emulator.run_program("300")
        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  AD  LDA    abs 00 10  01 00 00 FF 00100000\n" +
            " 302  AD  LDA    abs 00 10  01 00 00 FF 00100000\n" +
            " 304  AD  LDA    abs 00 10  01 00 00 FF 00100000\n" +
            " 305  AD  LDA    abs 00 10  01 00 00 FF 00100000\n" +
            " 306  AD  LDA    abs 00 10  01 00 00 FF 00100000\n" +
            " 308  AD  LDA    abs 00 10  01 00 00 FF 00100000\n" +
            " 30B  AD  LDA    abs 00 10  01 00 00 FF 00100000\n" +
            " 30D  AD  LDA    abs 00 10  01 00 00 FF 00100000\n" +
            " 30F  AD  LDA    abs 00 10  01 00 00 FF 00100000\n" +
            " 310  AD  LDA    abs 00 10  01 00 00 FF 00100000\n" +
            " 30F  AD  LDA    abs 00 10  01 00 00 FF 00100000\n" +
            " 310  AD  LDA    abs 00 10  01 00 00 FF 00100000\n" +
            " 30F  AD  LDA    abs 00 10  01 00 00 FF 00100000\n" +
            " 310  AD  LDA    abs 00 10  01 00 00 FF 00100000\n" +
            " 312  AD  LDA    abs 00 10  01 00 00 FF 00100000\n" +
            " 313  AD  LDA    abs 00 10  01 00 00 FF 00100000\n" +
            " 30D  AD  LDA    abs 00 10  01 00 00 FF 00100000\n" +
            " 310  AD  LDA    abs 00 10  01 00 00 FF 00100000\n" +
            " 30F  00  BRK   impl -- --  8E 00 00 FC 11110100\n")
