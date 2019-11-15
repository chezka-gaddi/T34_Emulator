from . import Memory


class Instructions(Memory.Memory):

    def __init__(self):
        super().__init__()
        self.name = ""
        self.instructions = {
            "00": self.brk,
            "08": self.php,
            "0A": self.asl,
            "18": self.clc,
            "28": self.plp,
            "2A": self.rol,
            "38": self.sec,
            "48": self.pha,
            "4A": self.lsr,
            "58": self.cli,
            "68": self.pla,
            "6A": self.ror,
            "78": self.sei,
            "88": self.dey,
            "8A": self.txa,
            "98": self.tya,
            "9A": self.txs,
            "B8": self.clv,
            "A8": self.tay,
            "AA": self.tax,
            "BA": self.tsx,
            "C8": self.iny,
            "CA": self.dex,
            "D8": self.cld,
            "E8": self.inx,
            "EA": self.nop,
            "F8": self.sed
        }

    def asl(self):
        ac = self.registers[3:4]
        carry = (ac & 1 << 7) >> 7
        if carry == 0:
            self.clc()
        else:
            self.sec()
        ac = ac << 1
        self.registers[3:4] = ac
        return "ASL", "A"

    def brk(self):
        self.sei()
        sp = int(self.registers[5:6].hex(), 16)
        pc = int(self.registers[:2].hex(), 16) + 2
        self.memory[sp:sp+2] = pc.to_bytes(2, byteorder='big')
        sp -= 2
        sr = int(self.registers[6:7].hex(), 16)
        self.memory[sp:sp+1] = sr.to_bytes(1, byteorder='big')
        sp -= 1
        self.registers[5:6] = sp.to_bytes(1, byteorder='big')

        sr = sr | (1 << 4)
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')
        return "BRK", "impl"

    def clc(self):
        sr = ~int(self.registers[6:7].hex(), 16) & 1
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')
        return "CLC", "impl"

    def cld(self):
        sr = ~int(self.registers[6:7].hex(), 16) & (1 << 3)
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')
        return "CLD", "impl"

    def cli(self):
        sr = ~int(self.registers[6:7].hex(), 16) & (1 << 2)
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')
        return "CLI", "impl"

    def clv(self):
        sr = ~int(self.registers[6:7].hex(), 16) & (1 << 6)
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')
        return "CLV", "impl"

    def dex(self):
        x = int(self.registers[3:4].hex().upper(), 16) - 1
        self.registers[3:4] = x.to_bytes(1, byteorder='big')
        return "DEX", "impl"

    def dey(self):
        y = int(self.registers[4:5].hex().upper(), 16) - 1
        self.registers[4:5] = y.to_bytes(1, byteorder='big')
        return "DEY", "impl"

    def inx(self):
        x = int(self.registers[3:4].hex().upper(), 16) + 1
        self.registers[3:4] = x.to_bytes(1, byteorder='big')
        return "INX", "impl"

    def iny(self):
        y = int(self.registers[4:5].hex().upper(), 16) + 1
        self.registers[4:5] = y.to_bytes(1, byteorder='big')
        return "INY", "impl"

    def lsr(self):
        ac = int(self.registers[2:3].hex().upper(), 16)
        ac = ac >> 1
        self.registers[2:3] = ac.to_bytes(1, byteorder='big')
        return "LSR", "A"

    def nop(self):
        return "NOP", "impl"

    def pha(self):
        sp = int(self.registers[5:6].hex(), 16)
        self.memory[sp:sp+1] = self.registers[2:3]
        sp -= 1
        self.registers[5:6] = sp.to_bytes(1, byteorder='big')
        return "PHA", "impl"

    def php(self):
        """Pushes a copy of the status flags on to the stack."""
        sp = int(self.registers[5:6].hex(), 16)
        sr = int(self.registers[6:7].hex(), 16)
        return "PHP", "impl"

    def pla(self):
        sp = int(self.registers[5:6].hex(), 16) + 1
        self.registers[2:3] = self.memory[sp:sp+1]
        self.registers[5:6] = sp.to_bytes(1, byteorder='big')
        return "PLA", "impl"

    def plp(self):
        return "PLP", "impl"

    def rol(self):
        return "ROL", "A"

    def ror(self):
        return "ROR", "A"

    def sec(self):
        sr = int(self.registers[6:7].hex(), 16) | 1
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')
        return "SEC", "impl"

    def sed(self):
        sr = int(self.registers[6:7].hex(), 16) | (1 << 3)
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')
        return "SED", "impl"

    def sei(self):
        sr = int(self.registers[6:7].hex(), 16) | (1 << 2)
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')
        return "SEI", "impl"

    def tax(self):
        self.registers[3:4] = self.registers[2:3]
        return "TAX", "impl"

    def tay(self):
        self.registers[4:5] = self.registers[2:3]
        return "TAY", "impl"

    def tsx(self):
        self.registers[3:4] = self.registers[5:6]
        return "TSX", "impl"

    def txa(self):
        self.registers[2:3] = self.registers[3:4]
        return "TXA", "impl"

    def txs(self):
        self.registers[5:6] = self.registers[3:4]
        return "TXS", "impl"

    def tya(self):
        self.registers[2:3] = self.registers[4:5]
        return "TYA", "impl"
