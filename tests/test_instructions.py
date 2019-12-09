"""
.. module:: TestInstructions
"""
import unittest
import t34
from t34.Emulator import Emulator


class TestInstructions(unittest.TestCase):
    """Unit testing class for all instructions in the Instructions class."""

    maxDiff = None

    def setUp(self):
        self.emulator = Emulator()

    def test_run_program_nop(self):
        """Test run program with no operand."""
        self.emulator.edit_memory("300", "EA C8 98 48 E8 E8 8A 68 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  C8  INY   impl -- --  00 00 01 FF 00100000\n" +
            " 302  98  TYA   impl -- --  01 00 01 FF 00100000\n" +
            " 303  48  PHA   impl -- --  01 00 01 FE 00100000\n" +
            " 304  E8  INX   impl -- --  01 01 01 FE 00100000\n" +
            " 305  E8  INX   impl -- --  01 02 01 FE 00100000\n" +
            " 306  8A  TXA   impl -- --  02 02 01 FE 00100000\n" +
            " 307  68  PLA   impl -- --  01 02 01 FF 00100000\n" +
            " 308  00  BRK   impl -- --  01 02 01 FC 00110100\n")

    def set_ac(self):
        """Sets ac to 4"""
        sp = int(self.emulator.registers[2:3].hex(), 16) | 4
        self.emulator.registers[2:3] = sp.to_bytes(1, byteorder='big')

    def test_asl(self):
        """Test asl instruction."""
        self.set_ac()
        self.emulator.edit_memory("300", "EA 0A 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  04 00 00 FF 00100000\n" +
            " 301  0A  ASL      A -- --  08 00 00 FF 00100000\n" +
            " 302  00  BRK   impl -- --  08 00 00 FC 00110100\n")

    def test_brk(self):
        self.set_ac()

    def test_clc(self):
        """Test clc instruction."""
        sr = int(self.emulator.registers[6:7].hex(), 16) | 1
        self.emulator.registers[6:7] = sr.to_bytes(1, byteorder='big')

        self.emulator.edit_memory("300", "EA 18 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100001\n" +
            " 301  18  CLC   impl -- --  00 00 00 FF 00100000\n" +
            " 302  00  BRK   impl -- --  00 00 00 FC 00110100\n")

    def test_cld(self):
        """Test cld instruction."""
        sr = int(self.emulator.registers[6:7].hex(), 16) | 8
        self.emulator.registers[6:7] = sr.to_bytes(1, byteorder='big')

        self.emulator.edit_memory("300", "EA D8 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00101000\n" +
            " 301  D8  CLD   impl -- --  00 00 00 FF 00100000\n" +
            " 302  00  BRK   impl -- --  00 00 00 FC 00110100\n")

    def test_cli(self):
        """Test cli instruction."""
        sr = int(self.emulator.registers[6:7].hex(), 16) | 4
        self.emulator.registers[6:7] = sr.to_bytes(1, byteorder='big')

        self.emulator.edit_memory("300", "EA 58 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100100\n" +
            " 301  58  CLI   impl -- --  00 00 00 FF 00100000\n" +
            " 302  00  BRK   impl -- --  00 00 00 FC 00110100\n")

    def test_clv(self):
        """Test clv instruction."""
        sr = int(self.emulator.registers[6:7].hex(), 16) | 64
        self.emulator.registers[6:7] = sr.to_bytes(1, byteorder='big')

        self.emulator.edit_memory("300", "EA B8 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 01100000\n" +
            " 301  B8  CLV   impl -- --  00 00 00 FF 00100000\n" +
            " 302  00  BRK   impl -- --  00 00 00 FC 00110100\n")

    def test_dex(self):
        """Test dex instruction."""
        sr = int(self.emulator.registers[3:4].hex(), 16) | 1
        self.emulator.registers[3:4] = sr.to_bytes(1, byteorder='big')

        self.emulator.edit_memory("300", "EA CA 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 01 00 FF 00100000\n" +
            " 301  CA  DEX   impl -- --  00 00 00 FF 00100010\n" +
            " 302  00  BRK   impl -- --  00 00 00 FC 00110110\n")

    def test_dex_xnegative(self):
        """Test dex to negative instruction."""
        self.emulator.edit_memory("300", "EA CA 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  CA  DEX   impl -- --  00 FF 00 FF 10100000\n" +
            " 302  00  BRK   impl -- --  00 FF 00 FC 10110100\n")

    def test_dey(self):
        """Test dey instruction."""
        sr = int(self.emulator.registers[4:5].hex(), 16) | 1
        self.emulator.registers[4:5] = sr.to_bytes(1, byteorder='big')

        self.emulator.edit_memory("300", "EA 88 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 01 FF 00100000\n" +
            " 301  88  DEY   impl -- --  00 00 00 FF 00100010\n" +
            " 302  00  BRK   impl -- --  00 00 00 FC 00110110\n")

    def test_dey_ynegative(self):
        """Test dey to negative instruction."""
        self.emulator.edit_memory("300", "EA 88 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  88  DEY   impl -- --  00 00 FF FF 10100000\n" +
            " 302  00  BRK   impl -- --  00 00 FF FC 10110100\n")

    def test_inx(self):
        """Test inx instruction."""
        sr = int(self.emulator.registers[3:4].hex(), 16) | 1
        self.emulator.registers[3:4] = sr.to_bytes(1, byteorder='big')

        self.emulator.edit_memory("300", "EA E8 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 01 00 FF 00100000\n" +
            " 301  E8  INX   impl -- --  00 02 00 FF 00100000\n" +
            " 302  00  BRK   impl -- --  00 02 00 FC 00110100\n")

    def test_iny(self):
        """Test iny instruction."""
        self.emulator.edit_memory("300", "EA C8 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  C8  INY   impl -- --  00 00 01 FF 00100000\n" +
            " 302  00  BRK   impl -- --  00 00 01 FC 00110100\n")

    def test_lsr(self):
        """Test lsr instruction."""
        ac = int(self.emulator.registers[2:3].hex(), 16) | 2
        self.emulator.registers[2:3] = ac.to_bytes(1, byteorder='big')

        self.emulator.edit_memory("300", "EA 4A 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  02 00 00 FF 00100000\n" +
            " 301  4A  LSR      A -- --  01 00 00 FF 00100000\n" +
            " 302  00  BRK   impl -- --  01 00 00 FC 00110100\n")

    def test_lsr_carry(self):
        """Test lsr instruction with carry."""
        ac = int(self.emulator.registers[2:3].hex(), 16) | 1
        self.emulator.registers[2:3] = ac.to_bytes(1, byteorder='big')

        self.emulator.edit_memory("300", "EA 4A 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  01 00 00 FF 00100000\n" +
            " 301  4A  LSR      A -- --  00 00 00 FF 00100011\n" +
            " 302  00  BRK   impl -- --  00 00 00 FC 00110111\n")

    def test_pha(self):
        """Test pha instruction."""
        ac = int(self.emulator.registers[2:3].hex(), 16) | 2
        self.emulator.registers[2:3] = ac.to_bytes(1, byteorder='big')

        self.emulator.edit_memory("300", "EA 48 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  02 00 00 FF 00100000\n" +
            " 301  48  PHA   impl -- --  02 00 00 FE 00100000\n" +
            " 302  00  BRK   impl -- --  02 00 00 FB 00110100\n")

    def test_php(self):
        """Test php instruction."""
        self.emulator.edit_memory("300", "EA 08 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  08  PHP   impl -- --  00 00 00 FE 00100000\n" +
            " 302  00  BRK   impl -- --  00 00 00 FB 00110100\n")

    def test_pla(self):
        """Test php instruction."""
        ac = int(self.emulator.registers[2:3].hex(), 16) | 2
        self.emulator.registers[2:3] = ac.to_bytes(1, byteorder='big')

        self.emulator.edit_memory("300", "EA 48 68 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  02 00 00 FF 00100000\n" +
            " 301  48  PHA   impl -- --  02 00 00 FE 00100000\n" +
            " 302  68  PLA   impl -- --  02 00 00 FF 00100000\n" +
            " 303  00  BRK   impl -- --  02 00 00 FC 00110100\n")

    def test_rol(self):
        """Test rol instruction."""
        ac = int(self.emulator.registers[2:3].hex(), 16) | 128
        self.emulator.registers[2:3] = ac.to_bytes(1, byteorder='big')

        self.emulator.edit_memory("300", "EA 2A 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  80 00 00 FF 00100000\n" +
            " 301  2A  ROL      A -- --  00 00 00 FF 00100011\n" +
            " 302  00  BRK   impl -- --  00 00 00 FC 00110111\n")

    def test_ror(self):
        """Test ror instruction."""
        ac = int(self.emulator.registers[2:3].hex(), 16) | 128
        self.emulator.registers[2:3] = ac.to_bytes(1, byteorder='big')

        self.emulator.edit_memory("300", "EA 6A 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  80 00 00 FF 00100000\n" +
            " 301  6A  ROR      A -- --  40 00 00 FF 00100000\n" +
            " 302  00  BRK   impl -- --  40 00 00 FC 00110100\n")

    def test_sec(self):
        """Test sec instruction."""
        self.emulator.edit_memory("300", "EA 38 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  38  SEC   impl -- --  00 00 00 FF 00100001\n" +
            " 302  00  BRK   impl -- --  00 00 00 FC 00110101\n")

    def test_sed(self):
        """Test sed instruction."""
        self.emulator.edit_memory("300", "EA F8 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  F8  SED   impl -- --  00 00 00 FF 00101000\n" +
            " 302  00  BRK   impl -- --  00 00 00 FC 00111100\n")

    def test_sei(self):
        """Test sei instruction."""
        self.emulator.edit_memory("300", "EA 78 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  78  SEI   impl -- --  00 00 00 FF 00100100\n" +
            " 302  00  BRK   impl -- --  00 00 00 FC 00110100\n")

    def test_tax(self):
        """Test tax instruction."""
        ac = int(self.emulator.registers[2:3].hex(), 16) | 1
        self.emulator.registers[2:3] = ac.to_bytes(1, byteorder='big')

        self.emulator.edit_memory("300", "EA AA 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  01 00 00 FF 00100000\n" +
            " 301  AA  TAX   impl -- --  01 01 00 FF 00100000\n" +
            " 302  00  BRK   impl -- --  01 01 00 FC 00110100\n")

    def test_tay(self):
        """Test tay instruction."""
        ac = int(self.emulator.registers[2:3].hex(), 16) | 1
        self.emulator.registers[2:3] = ac.to_bytes(1, byteorder='big')

        self.emulator.edit_memory("300", "EA A8 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  01 00 00 FF 00100000\n" +
            " 301  A8  TAY   impl -- --  01 00 01 FF 00100000\n" +
            " 302  00  BRK   impl -- --  01 00 01 FC 00110100\n")

    def test_tsx(self):
        """Test tsx instruction."""
        self.emulator.edit_memory("300", "EA BA 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 00 FF 00100000\n" +
            " 301  BA  TSX   impl -- --  00 FF 00 FF 10100000\n" +
            " 302  00  BRK   impl -- --  00 FF 00 FC 10110100\n")

    def test_txa(self):
        """Test txa instruction."""
        x = int(self.emulator.registers[3:4].hex(), 16) | 1
        self.emulator.registers[3:4] = x.to_bytes(1, byteorder='big')

        self.emulator.edit_memory("300", "EA 8A 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 01 00 FF 00100000\n" +
            " 301  8A  TXA   impl -- --  01 01 00 FF 00100000\n" +
            " 302  00  BRK   impl -- --  01 01 00 FC 00110100\n")

    def test_txs(self):
        """Test txs instruction."""
        x = int(self.emulator.registers[3:4].hex(), 16) | 8
        self.emulator.registers[3:4] = x.to_bytes(1, byteorder='big')

        self.emulator.edit_memory("300", "EA 9A 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 08 00 FF 00100000\n" +
            " 301  9A  TXS   impl -- --  00 08 00 08 00100000\n" +
            " 302  00  BRK   impl -- --  00 08 00 05 00110100\n")

    def test_tya(self):
        """Test tya instruction."""
        y = int(self.emulator.registers[4:5].hex(), 16) | 1
        self.emulator.registers[4:5] = y.to_bytes(1, byteorder='big')

        self.emulator.edit_memory("300", "EA 98 00")
        output = self.emulator.run_program("300")

        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  EA  NOP   impl -- --  00 00 01 FF 00100000\n" +
            " 301  98  TYA   impl -- --  01 00 01 FF 00100000\n" +
            " 302  00  BRK   impl -- --  01 00 01 FC 00110100\n")

    # Test immediate intructions
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

    # def test_cmp_imm(self):
    #     """Test cmp imm instruction. FF-00"""
    #     self.emulator.edit_memory("300", "EA C9 00 00")

    #     self.emulator.write_AC(255)
    #     output = self.emulator.run_program("300")

    #     self.assertEqual(
    #         output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
    #         " 300  EA  NOP   impl -- --  FF 00 00 FF 10100000\n" +
    #         " 301  C9  CMP      # 00 --  FF 00 00 FF 10100001\n" +
    #         " 303  00  BRK   impl -- --  FF 00 00 FC 10110101\n")

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

    # Test zeropage instructions
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

    @unittest.skip("Haven't implemented compare instruction")
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

    # Test indirect and relative instructions
    def test_jmp_ind(self):
        """Test jmp ind instruction."""
        self.emulator.edit_memory("300", "6C 05 03 00")
        self.emulator.edit_memory("30A", "00")

        output = self.emulator.run_program("300")
        self.assertEqual(
            output, " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n" +
            " 300  6C  JMP    ind 05 03  00 00 00 FF 00100000\n" +
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

    # Test absolute instructions
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
