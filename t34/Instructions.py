"""
.. py:module:: Instructions
"""
from . import Memory
# :synopsis: Instructions class that maintains all of the instructions to be executed by the T34.


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

    def adc(self):
        """
        This instruction adds the contents of a memory location to the accumulator together with the carry bit. If overflow occurs the carry bit is set, this enables multiple byte addition to be performed.

        Processor Status after use:

        C - Set if overflow in bit 7
        Z - Set if A = 0
        I - Not affected
        D - Not affected
        B - Not affected
        V - Set if sign bit is incorrect
        N - Set if bit 7 set
        """

    def asl(self):
        """
        This operation shifts all the bits of the accumulator or memory contents one bit left. Bit 0 is set to 0 and bit 7 is placed in the carry flag. The effect of this operation is to multiply the memory contents by 2 (ignoring 2's complement considerations), setting the carry if the result will not fit in 8 bits.

        Processor Status after use:

        C - Set to contents of old bit 7
        Z - Set if A = 0
        I - Not affected
        D - Not affected
        B - Not affected
        V - Not affected
        N - Set if bit 7 of the result is set
        """
        ac = int(self.registers[2:3].hex(), 16)
        carry = (ac & (1 << 7)) >> 7

        if carry == 0:
            self.clc()
        else:
            self.sec()
        ac = ac << 1
        ac &= 0xFF
        self.check_zero(ac)
        self.check_negative(ac)
        self.registers[2:3] = ac.to_bytes(1, byteorder='big')
        return "ASL", "   A"

    def brk(self):
        """
        The BRK instruction forces the generation of an interrupt request. The program counter and processor status are pushed on the stack then the IRQ interrupt vector at $FFFE/F is loaded into the PC and the break flag in the status set to one.

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Set to 1
        V  	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        sp = int(self.registers[5:6].hex(), 16) + 256
        pc = int(self.registers[:2].hex(), 16) + 2

        # Push program counter to stack
        self.memory[sp:sp+2] = pc.to_bytes(2, byteorder='big')
        sp -= 2

        sr = int(self.registers[6:7].hex(), 16)

        # Set interrupt and break flags
        sr = sr | (1 << 2)
        sr = sr | (1 << 4)

        # Push current processor status to stack
        self.memory[sp:sp+1] = sr.to_bytes(1, byteorder='big')
        sp -= 1
        sp -= 256
        self.registers[5:6] = sp.to_bytes(1, byteorder='big')
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')
        return "BRK", "impl"

    def clc(self):
        """
        C = 0

        Set the carry flag to zero.

        C	Carry Flag	Set to 0
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        sr = int(self.registers[6:7].hex(), 16) & ~1
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')
        return "CLC", "impl"

    def cld(self):
        """
        D = 0

        Sets the decimal mode flag to zero.

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Set to 0
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        sr = int(self.registers[6:7].hex(), 16) & ~(1 << 3)
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')
        return "CLD", "impl"

    def cli(self):
        """
        I = 0

        Clears the interrupt disable flag allowing normal interrupt requests to be serviced.

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Set to 0
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        sr = int(self.registers[6:7].hex(), 16) & ~(1 << 2)
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')
        return "CLI", "impl"

    def clv(self):
        """
        V = 0

        Clears the overflow flag.

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Set to 0
        N	Negative Flag	Not affected
        """
        sr = int(self.registers[6:7].hex(), 16) & ~(1 << 6)
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')
        return "CLV", "impl"

    def dex(self):
        """
        X,Z,N = X-1

        Subtracts one from the X register setting the zero and negative flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if X is zero
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of X is set
        """
        x = int(self.registers[3:4].hex().upper(), 16) - 1
        self.check_zero(x)

        self.check_negative(x)
        if x < 0:
            x = 255
        self.registers[3:4] = x.to_bytes(1, byteorder='big')

        return "DEX", "impl"

    def dey(self):
        """
        Y,Z,N = Y-1

        Subtracts one from the Y register setting the zero and negative flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if Y is zero
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of Y is set
        """
        y = int(self.registers[4:5].hex().upper(), 16) - 1
        if y < 0:
            y = 255
        self.check_negative(y)
        self.check_zero(y)
        self.registers[4:5] = y.to_bytes(1, byteorder='big')
        return "DEY", "impl"

    def inx(self):
        """
        X,Z,N = X+1

        Adds one to the X register setting the zero and negative flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if X is zero
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of X is set
        """
        x = int(self.registers[3:4].hex(), 16) + 1
        sign = (x & (1 << 7)) >> 7
        self.check_zero(x)
        self.check_negative_sign(sign)
        if sign == 1:
            x = 255
        self.registers[3:4] = x.to_bytes(1, byteorder='big')
        return "INX", "impl"

    def iny(self):
        """
        Y,Z,N = Y+1

        Adds one to the Y register setting the zero and negative flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if Y is zero
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of Y is set
        """
        y = int(self.registers[4:5].hex(), 16) + 1
        self.check_zero(y)
        self.check_negative(y)
        if y < 0:
            y = 255
        self.registers[4:5] = y.to_bytes(1, byteorder='big')
        return "INY", "impl"

    def lsr(self):
        """
        LSR - Logical Shift Right

        A,C,Z,N = A/2 or M,C,Z,N = M/2

        Each of the bits in A or M is shift one place to the right. The bit that was in bit 0 is shifted into the carry flag. Bit 7 is set to zero.

        Processor Status after use:

        C	Carry Flag	Set to contents of old bit 0
        Z	Zero Flag	Set if result = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of the result is set
        """
        ac = int(self.registers[2:3].hex().upper(), 16)
        carry = (ac & 1)
        if carry == 0:
            self.clc()
        elif carry == 1:
            self.sec()

        ac = ac >> 1
        if ac == 0:
            self.set_zero()
        elif ac < 0:
            self.set_negative()
            ac = 255
        elif ac > 127:
            self.set_negative()
        self.registers[2:3] = ac.to_bytes(1, byteorder='big')
        return "LSR", "A"

    def nop(self):
        """
        NOP - No Operation
        The NOP instruction causes no changes to the processor other than the normal incrementing of the program counter to the next instruction.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        return "NOP", "impl"

    def pha(self):
        """
        PHA - Push Accumulator
        Pushes a copy of the accumulator on to the stack.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        sp = int(self.registers[5:6].hex(), 16)
        sp += 256
        # self.write_memory(sp, self.registers[2:3])
        self.memory[sp:sp+1] = self.registers[2:3]
        sp -= 1
        sp -= 256
        self.registers[5:6] = sp.to_bytes(1, byteorder='big')
        return "PHA", "impl"

    def php(self):
        """
        PHP - Push Processor Status
        Pushes a copy of the status flags on to the stack.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        sp = int(self.registers[5:6].hex(), 16)
        sp += 256
        self.memory[sp:sp+1] = self.registers[6:7]
        sp -= 1
        sp -= 256
        self.registers[5:6] = sp.to_bytes(1, byteorder='big')
        return "PHP", "impl"

    def pla(self):
        """
        PLA - Pull Accumulator
        Pulls an 8 bit value from the stack and into the accumulator. The zero and negative flags are set as appropriate.

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of A is set
        """
        sp = int(self.registers[5:6].hex(), 16) + 1
        sp += 256
        self.registers[2:3] = self.read_memory(sp, sp+1)
        sp -= 256
        self.registers[5:6] = sp.to_bytes(1, byteorder='big')
        return "PLA", "impl"

    def plp(self):
        """
        PLP - Pull Processor Status
        Pulls an 8 bit value from the stack and into the processor flags. The flags will take on new states as determined by the value pulled.

        Processor Status after use:

        C	Carry Flag	Set from stack
        Z	Zero Flag	Set from stack
        I	Interrupt Disable	Set from stack
        D	Decimal Mode Flag	Set from stack
        B	Break Command	Set from stack
        V	Overflow Flag	Set from stack
        N	Negative Flag	Set from stack
        """
        sp = int(self.registers[5:6].hex(), 16) + 1
        self.registers[5:6] = sp.to_bytes(1, byteorder='big')
        sp += 256
        self.registers[6:7] = self.read_memory(sp, sp+1)
        return "PLP", "impl"

    def rol(self):
        """
        ROL - Rotate Left
        Move each of the bits in either A or M one place to the left. Bit 0 is filled with the current value of the carry flag whilst the old bit 7 becomes the new carry flag value.

        Processor Status after use:

        C	Carry Flag	Set to contents of old bit 7
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of the result is set
        """
        ac = int(self.registers[2:3].hex(), 16)
        ov = (ac & (1 << 7)) >> 7
        ac = ac & ~(1 << 7)
        ac = ac << 1

        if self.carry_isSet():
            ac = ac | 1

        if ov == 0:
            self.clc()
        else:
            self.sec()

        if ac > 255:
            ac = 1
        self.check_negative(ac)
        self.check_zero(ac)
        self.registers[2:3] = ac.to_bytes(1, byteorder='big')
        return "ROL", "A"

    def ror(self):
        """
        ROR - Rotate Right
        Move each of the bits in either A or M one place to the right. Bit 7 is filled with the current value of the carry flag whilst the old bit 0 becomes the new carry flag value.

        Processor Status after use:

        C	Carry Flag	Set to contents of old bit 0
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of the result is set
        """
        ac = int(self.registers[2:3].hex(), 16)
        ov = ac & 1
        ac = ac >> 1

        if self.carry_isSet():
            ac = ac | (1 << 7)
        else:
            ac = ac & ~(1 << 7)

        if ov == 0:
            self.clc()
        else:
            self.sec()

        if ac > 255:
            ac = 1
        self.check_negative(ac)
        self.check_zero(ac)
        self.registers[2:3] = ac.to_bytes(1, byteorder='big')
        return "ROR", "A"

    def sec(self):
        """
        SEC - Set Carry Flag
        C = 1

        Set the carry flag to one.

        C	Carry Flag	Set to 1
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        sr = int(self.registers[6:7].hex(), 16) | 1
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')
        return "SEC", "impl"

    def sed(self):
        """
        SED - Set Decimal Flag
        D = 1

        Set the decimal mode flag to one.

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Set to 1
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        sr = int(self.registers[6:7].hex(), 16) | (1 << 3)
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')
        return "SED", "impl"

    def sei(self):
        """
        SEI - Set Interrupt Disable
        I = 1

        Set the interrupt disable flag to one.

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Set to 1
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        sr = int(self.registers[6:7].hex(), 16) | (1 << 2)
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')
        return "SEI", "impl"

    def tax(self):
        """
        TAX - Transfer Accumulator to X
        X = A

        Copies the current contents of the accumulator into the X register and sets the zero and negative flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if X = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of X is set
        """
        self.registers[3:4] = self.registers[2:3]
        ac = int(self.registers[2:3].hex(), 16)
        sign = (ac & (1 << 7)) >> 7
        self.check_zero(ac)
        self.check_negative_sign(sign)
        return "TAX", "impl"

    def tay(self):
        """
        TAY - Transfer Accumulator to Y
        Y = A

        Copies the current contents of the accumulator into the Y register and sets the zero and negative flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if Y = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of Y is set
        """
        self.registers[4:5] = self.registers[2:3]
        ac = int(self.registers[2:3].hex(), 16)
        sign = (ac & (1 << 7)) >> 7
        self.check_zero(ac)
        self.check_negative_sign(sign)
        return "TAY", "impl"

    def tsx(self):
        """
        TSX - Transfer Stack Pointer to X
        X = S

        Copies the current contents of the stack register into the X register and sets the zero and negative flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if X = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of X is set
        """
        self.registers[3:4] = self.registers[5:6]
        sp = int(self.registers[5:6].hex(), 16)
        sign = (sp & (1 << 7)) >> 7
        self.check_zero(sp)
        self.check_negative_sign(sign)
        return "TSX", "impl"

    def txa(self):
        """
        TXA - Transfer X to Accumulator
        A = X

        Copies the current contents of the X register into the accumulator and sets the zero and negative flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of A is set
        """
        self.registers[2:3] = self.registers[3:4]
        x = int(self.registers[3:4].hex(), 16)
        sign = (x & (1 << 7)) >> 7
        self.check_zero(x)
        self.check_negative_sign(sign)
        return "TXA", "impl"

    def txs(self):
        """
        TXS - Transfer X to Stack Pointer
        S = X

        Copies the current contents of the X register into the stack register.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        self.registers[5:6] = self.registers[3:4]
        return "TXS", "impl"

    def tya(self):
        """
        TYA - Transfer Y to Accumulator
        A = Y

        Copies the current contents of the Y register into the accumulator and sets the zero and negative flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of A is set
        """
        self.registers[2:3] = self.registers[4:5]
        y = int(self.registers[4:5].hex(), 16)
        sign = (y & (1 << 7)) >> 7
        self.check_zero(y)
        self.check_negative_sign(sign)
        return "TYA", "impl"
