"""
.. module:: TestInstructionsAbsolute
"""
import unittest
import t34
from t34.Emulator import Emulator


class TestInstructionsAbsolute(unittest.TestCase):
    """Unit testing class for of the absolute instructions in the Instructions class."""

    maxDiff = None

    def setUp(self):
        self.emulator = Emulator()

    def test_adc_abs(self):
        """Test adc abs instruction with overflow and carry. -122+(-94)"""
        self.emulator.edit_memory("300", "EA 6D 05 03 00")
        self.emulator.edit_memory("305", "86")

        self.emulator.write_AC(162)
        output = self.emulator.run_program("300")
        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  A2 00 00 FF 10100000\n" +
            " 301  6D  ADC    abs 05 03  28 00 00 FF 01100001\n" +
            " 304  00  BRK   impl -- --  28 00 00 FC 01110101\n")

        output = self.emulator.access_memory("305")
        self.assertEqual(output, "305\t86")

    def test_and_abs(self):
        """Test and abs instruction. 5&4"""
        self.emulator.edit_memory("300", "EA 2D 06 03 00")
        self.emulator.edit_memory("306", "05")

        self.emulator.write_AC(4)
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  04 00 00 FF 00100000\n" +
            " 301  2D  AND    abs 06 03  04 00 00 FF 00100000\n" +
            " 304  00  BRK   impl -- --  04 00 00 FC 00110100\n")

        output = self.emulator.access_memory("306")
        self.assertEqual(output, "306\t05")

    def test_asl_abs(self):
        """Test asl abs instruction."""
        self.emulator.edit_memory("300", "EA 0E 06 03 00")
        self.emulator.edit_memory("306", "05")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  0E  ASL    abs 06 03  00 00 00 FF 00100000\n" +
            " 304  00  BRK   impl -- --  00 00 00 FC 00110100\n")

        output = self.emulator.access_memory("306")
        self.assertEqual(output, "306\t0A")

    def test_bit_abs(self):
        """Test bit abs instruction."""
        self.emulator.edit_memory("300", "EA 2C 0A 03 00")
        self.emulator.edit_memory("30A", "00")

        self.emulator.write_AC(143)
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  8F 00 00 FF 10100000\n" +
            " 301  2C  BIT    abs 0A 03  8F 00 00 FF 00100010\n" +
            " 304  00  BRK   impl -- --  8F 00 00 FC 00110110\n")

    def test_dec_abs(self):
        """Test dec abs instruction."""
        self.emulator.edit_memory("300", "EA CE 06 03 00")
        self.emulator.edit_memory("306", "00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  CE  DEC    abs 06 03  00 00 00 FF 10100000\n" +
            " 304  00  BRK   impl -- --  00 00 00 FC 10110100\n")

        output = self.emulator.access_memory("306")
        self.assertEqual(output, "306\tFF")

    def test_eor_abs(self):
        """Test eor abs instruction. 5^4"""
        self.emulator.edit_memory("300", "EA 4D 06 03 00")
        self.emulator.edit_memory("306", "05")

        self.emulator.write_AC(4)
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  04 00 00 FF 00100000\n" +
            " 301  4D  EOR    abs 06 03  01 00 00 FF 00100000\n" +
            " 304  00  BRK   impl -- --  01 00 00 FC 00110100\n")

    def test_inc_abs(self):
        """Test inc abs instruction."""
        self.emulator.edit_memory("300", "EA EE 06 03 00")
        self.emulator.edit_memory("306", "FF")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  EE  INC    abs 06 03  00 00 00 FF 00100010\n" +
            " 304  00  BRK   impl -- --  00 00 00 FC 00110110\n")

        output = self.emulator.access_memory("306")
        self.assertEqual(output, "306\t00")

    def test_jmp_abs(self):
        """Test jmp abs instruction."""
        self.emulator.edit_memory("300", "4C 0A 03 00")
        self.emulator.edit_memory("30A", "00")

        output = self.emulator.run_program("300")
        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  4C  JMP    abs 0A 03  00 00 00 FF 00100000\n" +
            " 30A  00  BRK   impl -- --  00 00 00 FC 00110100\n")

    def test_jsr_abs(self):
        """Test jsr abs instruction."""
        self.emulator.edit_memory("300", "20 0A 03 00")
        self.emulator.edit_memory("30A", "60")

        output = self.emulator.run_program("300")
        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  20  JSR    abs 0A 03  00 00 00 FD 00100000\n" +
            " 30A  60  RTS   impl -- --  00 00 00 FF 00100000\n" +
            " 303  00  BRK   impl -- --  00 00 00 FC 00110100\n")

    def test_lda_abs(self):
        """Test lda abs instruction."""
        self.emulator.edit_memory("300", "EA AD 0A 03 00")
        self.emulator.edit_memory("30A", "01")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  AD  LDA    abs 0A 03  01 00 00 FF 00100000\n" +
            " 304  00  BRK   impl -- --  01 00 00 FC 00110100\n")

    def test_ldx_abs(self):
        """Test ldx abs instruction. 0 -> X, set zero flag, unset negative"""
        self.emulator.write_X(255)
        self.emulator.edit_memory("300", "EA AE 0A 03 00")
        self.emulator.edit_memory("30A", "00")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 FF 00 FF 10100000\n" +
            " 301  AE  LDX    abs 0A 03  00 00 00 FF 00100010\n" +
            " 304  00  BRK   impl -- --  00 00 00 FC 00110110\n")

    def test_ldy_abs(self):
        """Test ldx abs instruction. 0 -> Y, set zero flag, unset negative"""
        self.emulator.write_Y(255)
        self.emulator.edit_memory("300", "EA AC 0A 03 00")
        self.emulator.edit_memory("30A", "00")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 FF FF 10100000\n" +
            " 301  AC  LDY    abs 0A 03  00 00 00 FF 00100010\n" +
            " 304  00  BRK   impl -- --  00 00 00 FC 00110110\n")

    def test_lsr_abs(self):
        """5 -> 2, set carry"""
        self.emulator.edit_memory("300", "EA 4E 0A 03 00")

        self.emulator.write_memory("30A", 5)
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  4E  LSR    abs 0A 03  00 00 00 FF 00100001\n" +
            " 304  00  BRK   impl -- --  00 00 00 FC 00110101\n")

        output = self.emulator.access_memory("30A")
        self.assertEqual(output, "30A\t02")

    def test_ora_abs(self):
        """Test ora abs instruction. 194 | 169 -> A"""
        self.emulator.edit_memory("30A", "A9")
        self.emulator.edit_memory("300", "EA 0D 0A 03 00")

        self.emulator.write_AC(194)
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  C2 00 00 FF 10100000\n" +
            " 301  0D  ORA    abs 0A 03  EB 00 00 FF 10100000\n" +
            " 304  00  BRK   impl -- --  EB 00 00 FC 10110100\n")

    def test_rol_abs(self):
        """Test rol abs instruction. 01 -> 02"""
        self.emulator.edit_memory("30A", "01")
        self.emulator.edit_memory("300", "EA 2E 0A 03 00")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  2E  ROL    abs 0A 03  00 00 00 FF 00100000\n" +
            " 304  00  BRK   impl -- --  00 00 00 FC 00110100\n")

        output = self.emulator.access_memory("30A")

        self.assertEqual(output, "30A\t02")

    def test_ror_abs(self):
        """Test ror abs instruction. 01 -> 00"""
        self.emulator.edit_memory("30A", "01")
        self.emulator.edit_memory("300", "EA 6E 0A 03 00")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  6E  ROR    abs 0A 03  00 00 00 FF 00100011\n" +
            " 304  00  BRK   impl -- --  00 00 00 FC 00110111\n")

        output = self.emulator.access_memory("30A")

        self.assertEqual(output, "30A\t00")

    def test_sta_abs(self):
        """Test sta abs instruction. FF -> M"""
        self.emulator.write_AC(255)
        self.emulator.edit_memory("300", "EA 8D 0A 03 00")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  FF 00 00 FF 10100000\n" +
            " 301  8D  STA    abs 0A 03  FF 00 00 FF 10100000\n" +
            " 304  00  BRK   impl -- --  FF 00 00 FC 10110100\n")

        output = self.emulator.access_memory("30A")

        self.assertEqual(output, "30A\tFF")

    def test_stx_abs(self):
        """Test stx abs instruction. FF -> M"""
        self.emulator.write_X(255)
        self.emulator.edit_memory("300", "EA 8E 0A 03 00")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 FF 00 FF 10100000\n" +
            " 301  8E  STX    abs 0A 03  00 FF 00 FF 10100000\n" +
            " 304  00  BRK   impl -- --  00 FF 00 FC 10110100\n")

        output = self.emulator.access_memory("30A")

        self.assertEqual(output, "30A\tFF")

    def test_sty_abs(self):
        """Test sty abs instruction. FF -> M"""
        self.emulator.write_Y(255)
        self.emulator.edit_memory("300", "EA 8C 0A 03 00")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 FF FF 10100000\n" +
            " 301  8C  STY    abs 0A 03  00 00 FF FF 10100000\n" +
            " 304  00  BRK   impl -- --  00 00 FF FC 10110100\n")

        output = self.emulator.access_memory("30A")

        self.assertEqual(output, "30A\tFF")
