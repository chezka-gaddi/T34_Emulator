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
