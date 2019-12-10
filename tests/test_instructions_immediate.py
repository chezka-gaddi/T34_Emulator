"""
.. module:: TestInstructionsImmediate
"""
import unittest
import t34
from t34.Emulator import Emulator


class TestInstructionsImmediate(unittest.TestCase):
    """Unit testing class for all instructions in the Instructions class."""

    maxDiff = None

    def setUp(self):
        self.emulator = Emulator()

    def test_adc_imm_vc(self):
        """Test adc imm instruction with overflow and carry. -122+(-94)"""
        self.emulator.edit_memory("300", "EA 69 86 00")

        self.emulator.write_AC(162)
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  A2 00 00 FF 10100000\n" +
            " 301  69  ADC      # 86 --  28 00 00 FF 01100001\n" +
            " 303  00  BRK   impl -- --  28 00 00 FC 01110101\n")

    def test_adc_imm_nc(self):
        """Test adc imm instruction with negative and carry. -22+(-43)"""
        self.emulator.edit_memory("300", "EA 69 EA 00")

        self.emulator.write_AC(213)
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  D5 00 00 FF 10100000\n" +
            " 301  69  ADC      # EA --  BF 00 00 FF 10100001\n" +
            " 303  00  BRK   impl -- --  BF 00 00 FC 10110101\n")

    def test_adc_imm_nv(self):
        """Test adc imm instruction with negative and overflow. 113+25"""
        self.emulator.edit_memory("300", "EA 69 71 00")

        self.emulator.write_AC(25)
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  19 00 00 FF 00100000\n" +
            " 301  69  ADC      # 71 --  8A 00 00 FF 11100000\n" +
            " 303  00  BRK   impl -- --  8A 00 00 FC 11110100\n")

    def test_adc_imm_carry(self):
        """Test adc imm with hanging carry. -22+(-43)+1"""
        self.emulator.edit_memory("300", "EA 69 EA 00")

        self.emulator.write_AC(213)
        self.emulator.set_carry()
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  D5 00 00 FF 10100001\n" +
            " 301  69  ADC      # EA --  C0 00 00 FF 10100001\n" +
            " 303  00  BRK   impl -- --  C0 00 00 FC 10110101\n")

    def test_and_imm(self):
        """Test and imm instruction. 5&4"""
        self.emulator.edit_memory("300", "EA 29 05 00")

        self.emulator.write_AC(4)
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  04 00 00 FF 00100000\n" +
            " 301  29  AND      # 05 --  04 00 00 FF 00100000\n" +
            " 303  00  BRK   impl -- --  04 00 00 FC 00110100\n")

    def test_cmp_imm(self):
        """Test cmp imm instruction. FF-00"""
        self.emulator.edit_memory("300", "EA C9 00 00")

        self.emulator.write_AC(255)
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  FF 00 00 FF 10100000\n" +
            " 301  C9  CMP      # 00 --  FF 00 00 FF 00100001\n" +
            " 303  00  BRK   impl -- --  FF 00 00 FC 00110101\n")

    def test_eor_imm(self):
        """Test eor imm instruction. 5^4"""
        self.emulator.edit_memory("300", "EA 49 05 00")

        self.emulator.write_AC(4)
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  04 00 00 FF 00100000\n" +
            " 301  49  EOR      # 05 --  01 00 00 FF 00100000\n" +
            " 303  00  BRK   impl -- --  01 00 00 FC 00110100\n")

    def test_lda_imm(self):
        """Test lda imm instruction."""
        self.emulator.edit_memory("300", "EA A9 FF 00")

        self.emulator.write_AC(4)
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  04 00 00 FF 00100000\n" +
            " 301  A9  LDA      # FF --  FF 00 00 FF 10100000\n" +
            " 303  00  BRK   impl -- --  FF 00 00 FC 10110100\n")

    def test_ldx_imm(self):
        """Test ldx imm instruction."""
        self.emulator.edit_memory("300", "EA A2 FF 00")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  A2  LDX      # FF --  00 FF 00 FF 10100000\n" +
            " 303  00  BRK   impl -- --  00 FF 00 FC 10110100\n")

    def test_ldy_imm(self):
        """Test ldy imm instruction."""
        self.emulator.edit_memory("300", "EA A0 FF 00")

        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  A0  LDY      # FF --  00 00 FF FF 10100000\n" +
            " 303  00  BRK   impl -- --  00 00 FF FC 10110100\n")

    def test_ora_imm(self):
        """Test ora imm instruction."""
        self.emulator.edit_memory("300", "EA 09 A9 00")

        self.emulator.write_AC(194)
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  C2 00 00 FF 10100000\n" +
            " 301  09  ORA      # A9 --  EB 00 00 FF 10100000\n" +
            " 303  00  BRK   impl -- --  EB 00 00 FC 10110100\n")

    def test_sbc_imm(self):
        """Test sbc imm instruction."""
        self.emulator.edit_memory("300", "EA E9 FF 00")

        self.emulator.write_AC(9)
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  09 00 00 FF 00100000\n" +
            " 301  E9  SBC      # FF --  0A 00 00 FF 00100000\n" +
            " 303  00  BRK   impl -- --  0A 00 00 FC 00110100\n")

    def test_sbc_imm_carry(self):
        """Test sbc imm instruction. """
        self.emulator.edit_memory("300", "EA E9 01 00")

        self.emulator.write_AC(5)
        self.emulator.set_carry()
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  05 00 00 FF 00100001\n" +
            " 301  E9  SBC      # 01 --  05 00 00 FF 00100001\n" +
            " 303  00  BRK   impl -- --  05 00 00 FC 00110101\n")
