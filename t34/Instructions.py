from . import Memory


class Instructions(Memory.Memory):

    def __init__(self):
        super().__init__()
        self.name = ""
        self.instructions = {
            "00": self.brk,
            "o8": self.php,
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
        return "ASL", "A"

    def brk(self):
        return "BRK", "impl"

    def clc(self):
        return "CLC", "impl"

    def cld(self):
        return "CLD", "impl"

    def cli(self):
        return "CLI", "impl"

    def clv(self):
        return "CLV", "impl"

    def dex(self):
        return "DEX", "impl"

    def dey(self):
        return "DEY", "impl"

    def inx(self):
        return "INX", "impl"

    def iny(self):
        return "INY", "impl"

    def lsr(self):
        return "LSR", "A"

    def nop(self):
        return "NOP", "impl"

    def pha(self):
        return "PHA", "impl"

    def php(self):
        return "PHP", "impl"

    def pla(self):
        return "PLA", "impl"

    def plp(self):
        return "PLP", "impl"

    def rol(self):
        return "ROL", "A"

    def ror(self):
        return "ROR", "A"

    def sec(self):
        return "SEC", "impl"

    def sed(self):
        return "SED", "impl"

    def sei(self):
        return "SEI", "impl"

    def tax(self):
        return "TAX", "impl"

    def tay(self):
        return "TAY", "impl"

    def tsx(self):
        return "TSX", "impl"

    def txa(self):
        return "TXA", "impl"

    def txs(self):
        return "TXS", "impl"

    def tya(self):
        return "TYA", "impl"
