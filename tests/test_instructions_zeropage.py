"""
.. module:: TestInstructionsZeropage
"""
import unittest
import t34
from t34.Emulator import Emulator


class TestInstructionsZeropage(unittest.TestCase):
    """Unit testing class for all instructions in the Instructions class."""

    maxDiff = None

    def setUp(self):
        self.emulator = Emulator()

    def test_bit_zpg(self):
        """Test bit zpg instruction."""
        self.emulator.edit_memory("300", "EA 24 05 00")
        self.emulator.edit_memory("05", "FF")

        self.emulator.write_AC(143)
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  8F 00 00 FF 10100000\n" +
            " 301  24  BIT    zpg 05 --  8F 00 00 FF 11100000\n" +
            " 303  00  BRK   impl -- --  8F 00 00 FC 11110100\n")

    def test_eor_zpg(self):
        """Test eor zpg instruction. 5^4"""
        self.emulator.edit_memory("300", "EA 45 05 00")
        self.emulator.edit_memory("05", "05")

        self.emulator.write_AC(4)
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  04 00 00 FF 00100000\n" +
            " 301  45  EOR    zpg 05 --  01 00 00 FF 00100000\n" +
            " 303  00  BRK   impl -- --  01 00 00 FC 00110100\n")

    def test_dec_zpg(self):
        """Test dec zpg instruction."""
        self.emulator.edit_memory("300", "EA C6 05 00")
        self.emulator.edit_memory("05", "05")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  C6  DEC    zpg 05 --  00 00 00 FF 00100000\n" +
            " 303  00  BRK   impl -- --  00 00 00 FC 00110100\n")

        output = self.emulator.access_memory("05")
        self.assertEqual(output, "05\t04")

    def test_lda_zpg(self):
        """Test lda zpg instruction."""
        self.emulator.edit_memory("300", "EA A5 05 00")
        self.emulator.edit_memory("05", "01")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  A5  LDA    zpg 05 --  01 00 00 FF 00100000\n" +
            " 303  00  BRK   impl -- --  01 00 00 FC 00110100\n")

    def test_ldx_zpg(self):
        """Test ldx zpg instruction."""
        self.emulator.edit_memory("300", "EA A6 05 00")
        self.emulator.edit_memory("05", "FF")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  A6  LDX    zpg 05 --  00 FF 00 FF 10100000\n" +
            " 303  00  BRK   impl -- --  00 FF 00 FC 10110100\n")

    def test_ldy_zpg(self):
        """-1 -> Y, set negative"""
        self.emulator.edit_memory("300", "EA A4 05 00")
        self.emulator.edit_memory("05", "FF")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  A4  LDY    zpg 05 --  00 00 FF FF 10100000\n" +
            " 303  00  BRK   impl -- --  00 00 FF FC 10110100\n")

    def test_lsr_zpg(self):
        """Test lsr zpg instruction."""
        self.emulator.edit_memory("300", "EA 46 35 00")

        self.emulator.write_memory("35", 5)
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  46  LSR    zpg 35 --  00 00 00 FF 00100001\n" +
            " 303  00  BRK   impl -- --  00 00 00 FC 00110101\n")

        output = self.emulator.access_memory("35")
        self.assertEqual(output, "35\t02")

    def test_ora_zpg(self):
        """Test ora zpg instruction."""
        self.emulator.edit_memory("35", "A9")
        self.emulator.edit_memory("300", "EA 05 35 00")

        self.emulator.write_AC(194)
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  C2 00 00 FF 10100000\n" +
            " 301  05  ORA    zpg 35 --  EB 00 00 FF 10100000\n" +
            " 303  00  BRK   impl -- --  EB 00 00 FC 10110100\n")

    def test_rol_zpg(self):
        """Test rol zpg instruction."""
        self.emulator.edit_memory("35", "80")
        self.emulator.edit_memory("300", "EA 26 35 00")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  26  ROL    zpg 35 --  00 00 00 FF 00100011\n" +
            " 303  00  BRK   impl -- --  00 00 00 FC 00110111\n")

        output = self.emulator.access_memory("35")

        self.assertEqual(output, "35\t00")

    def test_ror_zpg(self):
        """Test ror zpg instruction."""
        self.emulator.edit_memory("35", "80")
        self.emulator.edit_memory("300", "EA 66 35 00")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  66  ROR    zpg 35 --  00 00 00 FF 00100000\n" +
            " 303  00  BRK   impl -- --  00 00 00 FC 00110100\n")

        output = self.emulator.access_memory("35")

        self.assertEqual(output, "35\t40")

    def test_sta_zpg(self):
        """Test sta zpg instruction."""
        self.emulator.write_AC(5)
        self.emulator.edit_memory("300", "EA 85 35 00")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  05 00 00 FF 00100000\n" +
            " 301  85  STA    zpg 35 --  05 00 00 FF 00100000\n" +
            " 303  00  BRK   impl -- --  05 00 00 FC 00110100\n")

        output = self.emulator.access_memory("35")

        self.assertEqual(output, "35\t05")

    def test_stx_zpg(self):
        """Test stx zpg instruction."""
        self.emulator.write_X(5)
        self.emulator.edit_memory("300", "EA 86 35 00")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 05 00 FF 00100000\n" +
            " 301  86  STX    zpg 35 --  00 05 00 FF 00100000\n" +
            " 303  00  BRK   impl -- --  00 05 00 FC 00110100\n")

        output = self.emulator.access_memory("35")

        self.assertEqual(output, "35\t05")

    def test_sty_zpg(self):
        """Test sty zpg instruction."""
        self.emulator.write_Y(5)
        self.emulator.edit_memory("300", "EA 84 35 00")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 05 FF 00100000\n" +
            " 301  84  STY    zpg 35 --  00 00 05 FF 00100000\n" +
            " 303  00  BRK   impl -- --  00 00 05 FC 00110100\n")

        output = self.emulator.access_memory("35")

        self.assertEqual(output, "35\t05")

    # Integration test of all immediate and zeropage instructions
    def test_immediate_and_zero(self):
        """Test immediate and zeropage instructions."""
        self.emulator.edit_memory("300", "69 10 A2 02 85 02 E6 02 A5 02 00")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  69  ADC      # 10 --  10 00 00 FF 00100000\n" +
            " 302  A2  LDX      # 02 --  10 02 00 FF 00100000\n" +
            " 304  85  STA    zpg 02 --  10 02 00 FF 00100000\n" +
            " 306  E6  INC    zpg 02 --  10 02 00 FF 00100000\n" +
            " 308  A5  LDA    zpg 02 --  11 02 00 FF 00100000\n" +
            " 30A  00  BRK   impl -- --  11 02 00 FC 00110100\n")

    def test_imm_with_cmp(self):
        """Test immediate with compare instructions."""
        self.emulator.edit_memory("300", "A9 AA 49 55 C9 00 69 01 C9 01")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  A9  LDA      # AA --  AA 00 00 FF 10100000\n" +
            " 302  49  EOR      # 55 --  FF 00 00 FF 10100000\n" +
            " 304  C9  CMP      # 00 --  FF 00 00 FF 00100001\n" +
            " 306  69  ADC      # 01 --  01 00 00 FF 00100001\n" +
            " 308  C9  CMP      # 01 --  01 00 00 FF 00100011\n" +
            " 30A  00  BRK   impl -- --  01 00 00 FC 00110111\n")

    def test_zeropage(self):
        """Test zeropage instructions."""
        self.emulator.edit_memory("000", "01 03 05 07 09 0B 0D 0F")
        self.emulator.edit_memory("300", "A5 02 25 07 A6 03 86 08 E6 08 46 00")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  A5  LDA    zpg 02 --  05 00 00 FF 00100000\n" +
            " 302  25  AND    zpg 07 --  05 00 00 FF 00100000\n" +
            " 304  A6  LDX    zpg 03 --  05 07 00 FF 00100000\n" +
            " 306  86  STX    zpg 08 --  05 07 00 FF 00100000\n" +
            " 308  E6  INC    zpg 08 --  05 07 00 FF 00100000\n" +
            " 30A  46  LSR    zpg 00 --  05 07 00 FF 00100011\n" +
            " 30C  00  BRK   impl -- --  05 07 00 FC 00110111\n")
