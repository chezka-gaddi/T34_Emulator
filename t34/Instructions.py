"""
.. module:: Instructions
    :synopsis: Instructions class that maintains all of the instructions to be executed by the T34.
"""
from . import Memory

import logging
logger = logging.getLogger(__name__)


class Instructions(Memory.Memory):
    """Class that handles all of the instructions to be executed by the T34."""

    def __init__(self):
        """Creates the dictionary that is used to execute instructions."""
        super().__init__()
        self.name = ""
        self.instructions = {
            "00": self.brk,
            "05": self.ora_zpg,
            "06": self.asl_zpg,
            "08": self.php,
            "09": self.ora_imm,
            "0A": self.asl,
            "0E": self.asl_abs,
            "0D": self.ora_abs,
            "10": self.bpl_rel,
            "18": self.clc,
            "20": self.jsr,
            "24": self.bit_zpg,
            "25": self.and_zpg,
            "26": self.rol_zpg,
            "28": self.plp,
            "29": self.and_imm,
            "2A": self.rol,
            "2C": self.bit_abs,
            "2D": self.and_abs,
            "2E": self.rol_abs,
            "30": self.bmi_rel,
            "38": self.sec,
            "45": self.eor_zpg,
            "46": self.lsr_zpg,
            "48": self.pha,
            "49": self.eor_imm,
            "4A": self.lsr,
            "4C": self.jmp_abs,
            "4D": self.eor_abs,
            "4E": self.lsr_abs,
            "50": self.bvc,
            "58": self.cli,
            "60": self.rts,
            "65": self.adc_zpg,
            "66": self.ror_zpg,
            "68": self.pla,
            "69": self.adc_imm,
            "6A": self.ror,
            "6C": self.jmp_ind,
            "6D": self.adc_abs,
            "6E": self.ror_abs,
            "70": self.bvs,
            "78": self.sei,
            "84": self.sty_zpg,
            "85": self.sta_zpg,
            "86": self.stx_zpg,
            "88": self.dey,
            "8A": self.txa,
            "8C": self.sty_abs,
            "8D": self.sta_abs,
            "8E": self.stx_abs,
            "90": self.bcc_rel,
            "98": self.tya,
            "9A": self.txs,
            "B8": self.clv,
            "A0": self.ldy_imm,
            "A2": self.ldx_imm,
            "A4": self.ldy_zpg,
            "A5": self.lda_zpg,
            "A6": self.ldx_zpg,
            "A8": self.tay,
            "A9": self.lda_imm,
            "AA": self.tax,
            "AC": self.ldy_abs,
            "AD": self.lda_abs,
            "AE": self.ldx_abs,
            "B0": self.bcs_rel,
            "BA": self.tsx,
            "C0": self.cpy_imm,
            "C4": self.cpy_zpg,
            "C5": self.cmp_zpg,
            "C6": self.dec_zpg,
            "C8": self.iny,
            "C9": self.cmp_imm,
            "CA": self.dex,
            "CC": self.cpy_abs,
            "CD": self.cmp_abs,
            "CE": self.dec_abs,
            "D0": self.bne_rel,
            "D8": self.cld,
            "E0": self.cpx_imm,
            "E4": self.cpx_zpg,
            "E5": self.sbc_zpg,
            "E6": self.inc_zpg,
            "E8": self.inx,
            "E9": self.sbc_imm,
            "EA": self.nop,
            "EC": self.cpx_abs,
            "ED": self.sbc_abs,
            "EE": self.inc_abs,
            "F0": self.beq_rel,
            "F8": self.sed
        }

    def adc_abs(self):
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
        address = bytearray(2)
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)

        address[0:1] = self.read_memory(mem_address+1, mem_address + 2)
        address[1:2] = self.read_memory(mem_address, mem_address + 1)
        mem_address = int(address.hex(), 16)

        mem_value = self.read_memory(mem_address, mem_address + 1).hex()
        mem_value = int(mem_value, 16)
        mem_sign, mem_value = self.check_negative(mem_value)
        ac = self.get_AC()
        ac_sign, ac = self.check_negative(ac)

        carry = 1 if self.carry_isSet() else 0

        logger.debug("Adding Immediate: " +
                     bin(ac) + " " + bin(mem_value) + " " + bin(carry))
        ac = ac + mem_value + carry

        new_ac_sign, ac = self.check_negative(ac)

        if ac_sign & mem_sign != new_ac_sign:
            logger.debug("Overflow")
            self.set_overflow()
        else:
            self.unset_overflow()

        if self.check_carry(ac):
            ac -= 256
        self.write_AC(ac)

        return "ADC", " abs", int(address[1:2].hex(), 16), int(address[0:1].hex(), 16)

    def adc_imm(self):
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
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        mem_value = self.read_memory(mem_address, mem_address + 1).hex()
        mem_value = int(mem_value, 16)
        mem_sign, mem_value = self.check_negative(mem_value)
        ac = self.get_AC()
        ac_sign, ac = self.check_negative(ac)

        carry = 1 if self.carry_isSet() else 0

        logger.debug("Adding Immediate: " +
                     bin(ac) + " " + bin(mem_value) + " " + bin(carry))
        ac = ac + mem_value + carry

        new_ac_sign, ac = self.check_negative(ac)

        if ac_sign & mem_sign != new_ac_sign:
            logger.debug("Overflow")
            self.set_overflow()
        else:
            self.unset_overflow()

        if self.check_carry(ac):
            ac -= 256
        self.write_AC(ac)

        return "ADC", "   #", mem_value

    def adc_zpg(self):
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
        # todo: Figure out if what I need to do is use the next number as the address to get the actual value
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        zpg_address = self.read_memory(mem_address, mem_address + 1).hex()
        zpg_address = int(zpg_address, 16)
        zpg_value = self.read_memory(zpg_address, zpg_address + 1).hex()
        zpg_value = int(zpg_value, 16)

        mem_sign, zpg_value = self.check_negative(zpg_value)
        ac = self.get_AC()
        ac_sign, ac = self.check_negative(ac)

        carry = 1 if self.carry_isSet() else 0

        logger.debug("Adding Immediate: " +
                     bin(ac) + " " + bin(zpg_value) + " " + bin(carry))
        ac = ac + zpg_value + carry

        new_ac_sign, ac = self.check_negative(ac)

        if ac_sign & mem_sign != new_ac_sign:
            logger.debug("Overflow")
            self.set_overflow()
        else:
            self.unset_overflow()

        if self.check_carry(ac):
            ac -= 256
        self.write_AC(ac)

        return "ADC", " zpg", zpg_address

    def and_abs(self):
        """
        A logical AND is performed, bit by bit, on the accumulator contents using the contents of a byte of memory.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 set
        """
        address = bytearray(2)
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)

        address[0:1] = self.read_memory(mem_address+1, mem_address + 2)
        address[1:2] = self.read_memory(mem_address, mem_address + 1)
        mem_address = int(address.hex(), 16)

        mem_value = self.read_memory(mem_address, mem_address + 1).hex()
        mem_value = int(mem_value, 16)
        ac = self.get_AC()

        ac = ac & mem_value

        self.write_AC(ac)
        return "AND", " abs", int(address[1:2].hex(), 16), int(address[0:1].hex(), 16)
    
    def and_imm(self):
        """
        A logical AND is performed, bit by bit, on the accumulator contents using the contents of a byte of memory.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        mem_value = self.read_memory(mem_address, mem_address + 1).hex()
        mem_value = int(mem_value, 16)
        ac = self.get_AC()

        ac = ac & mem_value

        self.write_AC(ac)
        return "AND", "   #", mem_value

    def and_zpg(self):
        """
        A logical AND is performed, bit by bit, on the accumulator contents using the contents of a byte of memory.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        zpg_address = self.read_memory(mem_address, mem_address + 1).hex()
        zpg_address = int(zpg_address, 16)
        zpg_value = self.read_memory(zpg_address, zpg_address + 1).hex()
        zpg_value = int(zpg_value, 16)

        ac = self.get_AC()

        ac = ac & zpg_value

        self.write_AC(ac)
        return "AND", " zpg", zpg_address

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
        _, ac = self.check_negative(ac)
        self.check_zero(ac)
        self.registers[2:3] = ac.to_bytes(1, byteorder='big')
        return "ASL", "   A"
    
    def asl_abs(self):
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
        address = bytearray(2)
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)

        address[0:1] = self.read_memory(mem_address+1, mem_address + 2)
        address[1:2] = self.read_memory(mem_address, mem_address + 1)
        mem_address = int(address.hex(), 16)

        mem_value = self.read_memory(mem_address, mem_address + 1).hex()
        mem_value = int(mem_value, 16)
        carry = (mem_value & (1 << 7)) >> 7

        if carry == 0:
            self.clc()
        else:
            self.sec()
        mem_value = mem_value << 1
        mem_value &= 0xFF
        _, mem_value = self.check_negative(mem_value)
        self.check_zero(mem_value)
        self.write_memory(mem_address, mem_value)
        return "ASL", " abs", int(address[1:2].hex(), 16), int(address[0:1].hex(), 16)

    def asl_zpg(self):
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
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        zpg_address = self.read_memory(mem_address, mem_address + 1).hex()
        zpg_address = int(zpg_address, 16)
        zpg_value = self.read_memory(zpg_address, zpg_address + 1).hex()
        zpg_value = int(zpg_value, 16)

        carry = (zpg_value & (1 << 7)) >> 7

        if carry == 0:
            self.clc()
        else:
            self.sec()

        zpg_value = zpg_value << 1
        zpg_value &= 0xFF
        _, zpg_value = self.check_negative(zpg_value)
        self.check_zero(zpg_value)
        self.write_memory(zpg_address, zpg_value)
        return "ASL", " zpg", zpg_address

    def bcc_rel(self):
        """
        BCC - Branch if Carry Clear

        If the carry flag is clear then add the relative displacement to the program counter to cause a branch to a new location.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        pc = self.get_PC()
        mem_address = pc + 1
        branch_displacement = self.read_memory(mem_address, mem_address + 1).hex()
        branch_displacement = int(branch_displacement, 16)

        offset = self.twos_complement(branch_displacement)

        if self.carry_isSet() is False:
            self.write_PC(mem_address + offset)

        return "BCC", " rel", branch_displacement
    
    def bcs_rel(self):
        """
        BCS - Branch if Carry Set

        If the carry flag is set then add the relative displacement to the program counter to cause a branch to a new location.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        pc = self.get_PC()
        mem_address = pc + 1
        branch_displacement = self.read_memory(mem_address, mem_address + 1).hex()
        branch_displacement = int(branch_displacement, 16)

        offset = self.twos_complement(branch_displacement)

        if self.carry_isSet():
            self.write_PC(mem_address + offset)

        return "BCS", " rel", branch_displacement
    
    def beq_rel(self):
        """
        BEQ - Branch on Result Zero

        If the zero flag is set then add the relative displacement to the program counter to cause a branch to a new location.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        pc = self.get_PC()
        mem_address = pc + 1
        branch_displacement = self.read_memory(mem_address, mem_address + 1).hex()
        branch_displacement = int(branch_displacement, 16)

        offset = self.twos_complement(branch_displacement)

        if self.zero_isSet():
            self.write_PC(mem_address + offset)

        return "BEQ", " rel", branch_displacement

    def bit_zpg(self):
        """
        A & M, N = M7, V = M6

        This instructions is used to test if one or more bits are set in a target memory location. The mask pattern in A is ANDed with the value in memory to set or clear the zero flag, but the result is not kept. Bits 7 and 6 of the value from memory are copied into the N and V flags.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if the result if the AND is zero
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Set to bit 6 of the memory value
        N	Negative Flag	Set to bit 7 of the memory value
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        zpg_address = self.read_memory(mem_address, mem_address + 1).hex()
        zpg_address = int(zpg_address, 16)
        zpg_value = self.read_memory(zpg_address, zpg_address + 1).hex()
        zpg_value = int(zpg_value, 16)

        ac = self.get_AC()
        value = ac & zpg_value

        if zpg_value & (1 << 6):
            self.set_overflow()
        else:
            self.unset_overflow()

        if zpg_value & (1 << 7):
            self.set_negative()
        else:
            self.unset_negative()
        self.check_zero(value)

        return "BIT", " zpg", zpg_address
    
    def bit_abs(self):
        """
        A & M, N = M7, V = M6

        This instructions is used to test if one or more bits are set in a target memory location. The mask pattern in A is ANDed with the value in memory to set or clear the zero flag, but the result is not kept. Bits 7 and 6 of the value from memory are copied into the N and V flags.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if the result if the AND is zero
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Set to bit 6 of the memory value
        N	Negative Flag	Set to bit 7 of the memory value
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)

        low, high, address = self.make_address(mem_address)

        mem_value = self.read_memory(address, address + 1).hex()
        mem_value = int(mem_value, 16)

        ac = self.get_AC()
        value = ac & mem_value

        if mem_value & (1 << 6):
            self.set_overflow()
        else:
            self.unset_overflow()

        if mem_value & (1 << 7):
            self.set_negative()
        else:
            self.unset_negative()
        self.check_zero(value)

        return "BIT", " abs", low, high

    def bmi_rel(self):
        """
        BMI - Branch if Minus

        If the negative flag is set then add the relative displacement to the program counter to cause a branch to a new location.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        pc = self.get_PC()
        mem_address = pc + 1
        branch_displacement = self.read_memory(mem_address, mem_address + 1).hex()
        branch_displacement = int(branch_displacement, 16)

        offset = self.twos_complement(branch_displacement)

        if self.negative_isSet():
            self.write_PC(mem_address + offset)

        return "BMI", " rel", branch_displacement
    
    def bne_rel(self):
        """
        BNE - Branch if Not Zero

        If the zero flag is not set then add the relative displacement to the program counter to cause a branch to a new location.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        pc = self.get_PC()
        mem_address = pc + 1
        branch_displacement = self.read_memory(mem_address, mem_address + 1).hex()
        branch_displacement = int(branch_displacement, 16)

        offset = self.twos_complement(branch_displacement)

        if self.zero_isSet() is False:
            self.write_PC(mem_address + offset)

        return "BNE", " rel", branch_displacement
    
    def bpl_rel(self):
        """
        BNE - Branch if Plus

        If the negative flag is not set then add the relative displacement to the program counter to cause a branch to a new location.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        pc = self.get_PC()
        mem_address = pc + 1
        branch_displacement = self.read_memory(mem_address, mem_address + 1).hex()
        branch_displacement = int(branch_displacement, 16)
        
        offset = self.twos_complement(branch_displacement)

        if self.negative_isSet() is False:
            self.write_PC(mem_address + offset)

        return "BPL", " rel", branch_displacement

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

    def bvc(self):
        """
        BVC - Branch on Overflow Clear

        If the overflow flag is not set then add the relative displacement to the program counter to cause a branch to a new location.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        pc = self.get_PC()
        mem_address = pc + 1
        branch_displacement = self.read_memory(mem_address, mem_address + 1).hex()
        branch_displacement = int(branch_displacement, 16)

        offset = self.twos_complement(branch_displacement)

        if self.overflow_isSet() is False:
            self.write_PC(mem_address + offset)

        return "BVC", " rel", branch_displacement
    
    def bvs(self):
        """
        BVS - Branch if Overflow Set

        If the overflow flag not set then add the relative displacement to the program counter to cause a branch to a new location.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        pc = self.get_PC()
        mem_address = pc + 1
        branch_displacement = self.read_memory(mem_address, mem_address + 1).hex()
        branch_displacement = int(branch_displacement, 16)
        
        offset = self.twos_complement(branch_displacement)

        if self.overflow_isSet():
            self.write_PC(mem_address + offset)

        return "BVS", " rel", branch_displacement
    
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

    def CMP(self, data1: int, data2: int):
        """Compares data1 with data2 and sets appropriate flags.
        
        Arguments:
            data1 {int} -- first data
            data2 {int} -- second data
        """
        logger.debug("Comparing " + str(data1) + " and " + str(data2))
        if data1 >= data2:
            logger.debug("Setting the carry flag")
            self.set_carry()
            self.unset_negative()
        else:
            sign, data2 = self.check_negative(data2)
            if sign:
                self.unset_carry()
        if data1 == data2:
            self.set_zero()

    def cmp_abs(self):
        """
        Z,C,N = A-M

        This instruction compares the contents of the accumulator with another memory held value and sets the zero and carry flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Set if A >= M
        Z	Zero Flag	Set if A = M
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of the result is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)

        low, high, address = self.make_address(mem_address)

        mem_value = self.read_memory(address, address + 1).hex()
        mem_value = int(mem_value, 16)

        ac = self.get_AC()

        self.CMP(ac, mem_value)

        return "CMP", " abs", low, high

    def cmp_imm(self):
        """
        Z,C,N = A-M

        This instruction compares the contents of the accumulator with another memory held value and sets the zero and carry flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Set if A >= M
        Z	Zero Flag	Set if A = M
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of the result is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        mem_value = self.read_memory(mem_address, mem_address + 1).hex()
        mem_value = int(mem_value, 16)
        ac = self.get_AC()

        logger.debug("Comparing " + str(ac) + " and " + str(mem_value))
        if ac >= mem_value:
            logger.debug("Setting the carry flag")
            self.set_carry()
            self.unset_negative()
        else:
            sign, mem_value = self.check_negative(mem_value)
            if sign:
                self.unset_carry()
        if ac == mem_value:
            self.set_zero()

        return "CMP", "   #", mem_value

    def cmp_zpg(self):
        """
        Z,C,N = A-M

        This instruction compares the contents of the accumulator with another memory held value and sets the zero and carry flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Set if A >= M
        Z	Zero Flag	Set if A = M
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of the result is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        zpg_address = self.read_memory(mem_address, mem_address + 1).hex()
        zpg_address = int(zpg_address, 16)
        zpg_value = self.read_memory(zpg_address, zpg_address + 1).hex()
        
        zpg_value = int(zpg_value, 16)
        ac = self.get_AC()

        logger.debug("Comparing " + str(ac) + " and " + str(zpg_value))
        if ac >= zpg_value:
            logger.debug("Setting the carry flag")
            self.set_carry()
            self.unset_negative()
        else:
            sign, zpg_value = self.check_negative(zpg_value)
            if sign:
                self.unset_carry()
        if ac == zpg_value:
            self.set_zero()

        return "CMP", " zpg", zpg_address
    
    def cpx_abs(self):
        """
        Z,C,N = X-M

        This instruction compares the contents of the x register with another memory held value and sets the zero and carry flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Set if X >= M
        Z	Zero Flag	Set if X = M
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of the result is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)

        low, high, address = self.make_address(mem_address)

        mem_value = self.read_memory(address, address + 1).hex()
        mem_value = int(mem_value, 16)

        x = self.get_X()

        self.CMP(x, mem_value)

        return "CPX", " abs", low, high

    def cpx_imm(self):
        """
        Z,C,N = X-M

        This instruction compares the contents of the X register with another memory held value and sets the zero and carry flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Set if X >= M
        Z	Zero Flag	Set if X = M
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of the result is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        mem_value = self.read_memory(mem_address, mem_address + 1).hex()
        mem_value = int(mem_value, 16)
        x = self.get_X()

        logger.debug("Comparing " + str(x) + " and " + str(mem_value))
        if x >= mem_value:
            logger.debug("Setting the carry flag")
            self.set_carry()
            self.unset_negative()
        else:
            sign, mem_value = self.check_negative(mem_value)
            if sign:
                self.unset_carry()
        if x == mem_value:
            self.set_zero()

        return "CPX", "   #", mem_value

    def cpx_zpg(self):
        """
        Z,C,N = X-M

        This instruction compares the contents of the X register with another memory held value and sets the zero and carry flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Set if X >= M
        Z	Zero Flag	Set if X = M
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of the result is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        zpg_address = self.read_memory(mem_address, mem_address + 1).hex()
        zpg_address = int(zpg_address, 16)
        zpg_value = self.read_memory(zpg_address, zpg_address + 1).hex()
        
        zpg_value = int(zpg_value, 16)
        x = self.get_X()

        logger.debug("Comparing " + str(x) + " and " + str(zpg_value))
        if x >= zpg_value:
            logger.debug("Setting the carry flag")
            self.set_carry()
            self.unset_negative()
        else:
            sign, zpg_value = self.check_negative(zpg_value)
            if sign:
                self.unset_carry()
        if x == zpg_value:
            self.set_zero()

        return "CPX", " zpg", zpg_address
    
    def cpy_abs(self):
        """
        Z,C,N = Y-M

        This instruction compares the contents of the y register with another memory held value and sets the zero and carry flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Set if Y >= M
        Z	Zero Flag	Set if Y = M
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of the result is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)

        low, high, address = self.make_address(mem_address)

        mem_value = self.read_memory(address, address + 1).hex()
        mem_value = int(mem_value, 16)

        y = self.get_Y()

        self.CMP(y, mem_value)

        return "CPY", " abs", low, high

    def cpy_imm(self):
        """
        Z,C,N = Y-M

        This instruction compares the contents of the Y register with another memory held value and sets the zero and carry flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Set if Y >= M
        Z	Zero Flag	Set if Y = M
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of the result is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        mem_value = self.read_memory(mem_address, mem_address + 1).hex()
        mem_value = int(mem_value, 16)
        y = self.get_Y()

        logger.debug("Comparing " + str(y) + " and " + str(mem_value))
        if y >= mem_value:
            logger.debug("Setting the carry flag")
            self.set_carry()
            self.unset_negative()
        else:
            sign, mem_value = self.check_negative(mem_value)
            if sign:
                self.unset_carry()
        if y == mem_value:
            self.set_zero()

        return "CPY", "   #", mem_value

    def cpy_zpg(self):
        """
        Z,C,N = Y-M

        This instruction compares the contents of the Y register with another memory held value and sets the zero and carry flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Set if Y >= M
        Z	Zero Flag	Set if Y = M
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of the result is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        zpg_address = self.read_memory(mem_address, mem_address + 1).hex()
        zpg_address = int(zpg_address, 16)
        zpg_value = self.read_memory(zpg_address, zpg_address + 1).hex()
        
        zpg_value = int(zpg_value, 16)
        y = self.get_Y()

        logger.debug("Comparing " + str(y) + " and " + str(zpg_value))
        if y >= zpg_value:
            logger.debug("Setting the carry flag")
            self.set_carry()
            self.unset_negative()
        else:
            sign, zpg_value = self.check_negative(zpg_value)
            if sign:
                self.unset_carry()
        if y == zpg_value:
            self.set_zero()

        return "CPY", " zpg", zpg_address

    def dec_abs(self):
        """
        M,Z,N = M-1

        Subtracts one from the value held at a specified memory location setting the zero and negative flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if result is zero
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of the result is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)
        
        low, high, address = self.make_address(mem_address)
        value = self.read_memory(address, address + 1).hex()
        value = int(value, 16)

        value -= 1
        _, value = self.check_negative(value)
        self.check_zero(value)
        self.write_memory(address, value)

        return "DEC", " abs", low, high

    def dec_zpg(self):
        """
        M,Z,N = M-1

        Subtracts one from the value held at a specified memory location setting the zero and negative flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if result is zero
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of the result is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        zpg_address = self.read_memory(mem_address, mem_address + 1).hex()
        zpg_address = int(zpg_address, 16)
        zpg_value = self.read_memory(zpg_address, zpg_address + 1).hex()
        zpg_value = int(zpg_value, 16)

        zpg_value -= 1
        _, zpg_value = self.check_negative(zpg_value)
        self.check_zero(zpg_value)
        self.write_memory(zpg_address, zpg_value)

        return "DEC", " zpg", zpg_address

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

        _, x = self.check_negative(x)
        self.check_zero(x)
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
        _, y = self.check_negative(y)
        self.check_zero(y)
        self.registers[4:5] = y.to_bytes(1, byteorder='big')
        return "DEY", "impl"
    
    def eor_abs(self):
        """
        A,Z,N = A^M

        An exclusive OR is performed, bit by bit, on the accumulator contents using the contents of a byte of memory.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)
        
        low, high, address = self.make_address(mem_address)
        value = self.read_memory(address, address + 1).hex()
        value = int(value, 16)
        ac = self.get_AC()

        ac = ac ^ value
        self.write_AC(ac)
        return "EOR", " abs", low, high

    def eor_imm(self):
        """
        A,Z,N = A^M

        An exclusive OR is performed, bit by bit, on the accumulator contents using the contents of a byte of memory.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        mem_value = self.read_memory(mem_address, mem_address + 1).hex()
        mem_value = int(mem_value, 16)
        ac = self.get_AC()

        ac = ac ^ mem_value
        self.write_AC(ac)
        return "EOR", "   #", mem_value

    def eor_zpg(self):
        """
        A,Z,N = A^M

        An exclusive OR is performed, bit by bit, on the accumulator contents using the contents of a byte of memory.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        zpg_address = self.read_memory(mem_address, mem_address + 1).hex()
        zpg_address = int(zpg_address, 16)
        zpg_value = self.read_memory(zpg_address, zpg_address + 1).hex()
        zpg_value = int(zpg_value, 16)
        ac = self.get_AC()

        ac = ac ^ zpg_value
        self.write_AC(ac)
        return "EOR", " zpg", zpg_address

    def inc_abs(self):
        """
        M,Z,N = M+1

        Adds one from the value held at a specified memory location setting the zero and negative flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if result is zero
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of the result is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)
        
        low, high, address = self.make_address(mem_address)
        value = self.read_memory(address, address + 1).hex()
        value = int(value, 16)

        value += 1
        _, value = self.check_negative(value)
        self.check_zero(value)
        self.write_memory(address, value)

        return "INC", " abs", low, high

    def inc_zpg(self):
        """
        M,Z,N = M+1

        Adds one to the value held at a specified memory location setting the zero and negative flags as appropriate.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if result is zero
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of the result is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        zpg_address = self.read_memory(mem_address, mem_address + 1).hex()
        zpg_address = int(zpg_address, 16)
        zpg_value = self.read_memory(zpg_address, zpg_address + 1).hex()
        zpg_value = int(zpg_value, 16)

        zpg_value += 1
        _, zpg_value = self.check_negative(zpg_value)
        self.check_zero(zpg_value)
        self.write_memory(zpg_address, zpg_value)

        return "INC", " zpg", zpg_address

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
        self.check_negative_sign(sign)
        self.check_zero(x)
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
        _, y = self.check_negative(y)
        self.check_zero(y)
        if y < 0:
            y = 255
        self.registers[4:5] = y.to_bytes(1, byteorder='big')
        return "INY", "impl"

    def jmp_abs(self):
        """
        JMP - Jump
        
        Sets the program counter to the address specified by the operand.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+2)
        
        low, high, address = self.make_address(mem_address)
        
        self.write_PC(address-1)

        return "JMP", " abs", low, high

    def jmp_ind(self):
        """
        JMP - Jump
        
        Sets the program counter to the address specified by the operand.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)
        
        low, high, address = self.make_address(mem_address)
        
        jump_address = bytearray(2)
        jump_address[1:2] = self.read_memory(address, address + 1)
        jump_address[0:1] = self.read_memory(address + 1, address + 2)

        self.write_PC(int(jump_address.hex(), 16)-1)

        return "JMP", " ind", low, high

    def jsr(self):
        """JSR - Jump to Subroutine
        
        The JSR instruction pushes the address (minus one) of the return point on to the stack and then sets the program counter to the target memory address.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        mem_address = self.get_PC()
        low, high, address = self.make_address(mem_address + 1)

        logger.debug("Pushing " + str(mem_address - 1) + " onto the stack")
        self.push_to_stack(mem_address + 2, 2)
        self.write_PC(address - 1)

        return "JSR", " abs", low, high

    def lda_abs(self):
        """
        A,Z,N = M

        Loads a byte of memory into the accumulator setting the zero and negative flags as appropriate.

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of A is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)
        
        low, high, address = self.make_address(mem_address)
        value = self.read_memory(address, address + 1).hex()
        value = int(value, 16)

        self.write_AC(value)

        return "LDA", " abs", low, high
    
    def lda_imm(self):
        """
        A,Z,N = M

        Loads a byte of memory into the accumulator setting the zero and negative flags as appropriate.

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of A is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        mem_value = self.read_memory(mem_address, mem_address + 1).hex()
        mem_value = int(mem_value, 16)

        self.write_AC(mem_value)

        return "LDA", "   #", mem_value
    
    def ldx_abs(self):
        """
        X,Z,N = M

        Loads a byte of memory into the x register setting the zero and negative flags as appropriate.

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of A is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)
        
        low, high, address = self.make_address(mem_address)
        value = self.read_memory(address, address + 1).hex()
        value = int(value, 16)

        self.write_X(value)

        return "LDX", " abs", low, high

    def lda_zpg(self):
        """
        A,Z,N = M

        Loads a byte of memory into the accumulator setting the zero and negative flags as appropriate.

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of A is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        zpg_address = self.read_memory(mem_address, mem_address + 1).hex()
        zpg_address = int(zpg_address, 16)
        zpg_value = self.read_memory(zpg_address, zpg_address + 1).hex()
        zpg_value = int(zpg_value, 16)

        self.write_AC(zpg_value)

        return "LDA", " zpg", zpg_address

    def ldx_imm(self):
        """
        X,Z,N = M

        Loads a byte of memory into the X register setting the zero and negative flags as appropriate.

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if X = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of X is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        mem_value = self.read_memory(mem_address, mem_address + 1).hex()
        mem_value = int(mem_value, 16)

        self.write_X(mem_value)

        return "LDX", "   #", mem_value

    def ldx_zpg(self):
        """
        X,Z,N = M

        Loads a byte of memory into the X register setting the zero and negative flags as appropriate.

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if X = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of X is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        zpg_address = self.read_memory(mem_address, mem_address + 1).hex()
        zpg_address = int(zpg_address, 16)
        zpg_value = self.read_memory(zpg_address, zpg_address + 1).hex()
        zpg_value = int(zpg_value, 16)

        self.write_X(zpg_value)

        return "LDX", " zpg", zpg_address

    def ldy_abs(self):
        """
        Y,Z,N = M

        Loads a byte of memory into the Y register setting the zero and negative flags as appropriate.

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of Y is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)
        
        low, high, address = self.make_address(mem_address)
        value = self.read_memory(address, address + 1).hex()
        value = int(value, 16)

        self.write_Y(value)

        return "LDY", " abs", low, high

    def ldy_imm(self):
        """
        Y,Z,N = M

        Loads a byte of memory into the Y register setting the zero and negative flags as appropriate.

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if Y = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of Y is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        mem_value = self.read_memory(mem_address, mem_address + 1).hex()
        mem_value = int(mem_value, 16)

        self.write_Y(mem_value)

        return "LDY", "   #", mem_value

    def ldy_zpg(self):
        """
        Y,Z,N = M

        Loads a byte of memory into the Y register setting the zero and negative flags as appropriate.

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if Y = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 of Y is set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        zpg_address = self.read_memory(mem_address, mem_address + 1).hex()
        zpg_address = int(zpg_address, 16)
        zpg_value = self.read_memory(zpg_address, zpg_address + 1).hex()
        zpg_value = int(zpg_value, 16)

        self.write_Y(zpg_value)

        return "LDY", " zpg", zpg_address

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
    
    def lsr_abs(self):
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
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)
        
        low, high, address = self.make_address(mem_address)
        value = self.read_memory(address, address + 1).hex()
        value = int(value, 16)

        carry = (value & 1)
        if carry == 0:
            self.unset_carry()
        elif carry == 1:
            self.set_carry()

        value = value >> 1
        self.check_zero(value)
        self.write_memory(address, value)

        return "LSR", " abs", low, high

    def lsr_zpg(self):
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
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        zpg_address = self.read_memory(mem_address, mem_address + 1).hex()
        zpg_address = int(zpg_address, 16)
        zpg_value = self.read_memory(zpg_address, zpg_address + 1).hex()
        zpg_value = int(zpg_value, 16)

        carry = (zpg_value & 1)
        if carry == 0:
            self.unset_carry()
        elif carry == 1:
            self.set_carry()

        zpg_value = zpg_value >> 1
        self.check_zero(zpg_value)
        self.write_memory(zpg_address, zpg_value)

        return "LSR", " zpg", zpg_address
    
    def ora_abs(self):
        """
        A,Z,N = A|M

        An inclusive OR is performed, bit by bit, on the accumulator contents using the contents of a byte of memory.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)
        
        low, high, address = self.make_address(mem_address)
        value = self.read_memory(address, address + 1).hex()
        value = int(value, 16)

        ac = self.get_AC()
        ac = ac | value
        self.write_AC(ac)

        return "ORA", " abs", low, high

    def ora_imm(self):
        """
        A,Z,N = A|M

        An inclusive OR is performed, bit by bit, on the accumulator contents using the contents of a byte of memory.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        mem_value = self.read_memory(mem_address, mem_address + 1).hex()
        mem_value = int(mem_value, 16)

        ac = self.get_AC()
        ac = ac | mem_value
        self.write_AC(ac)

        return "ORA", "   #", mem_value
    
    def ora_zpg(self):
        """
        A,Z,N = A|M

        An inclusive OR is performed, bit by bit, on the accumulator contents using the contents of a byte of memory.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Set if bit 7 set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        zpg_address = self.read_memory(mem_address, mem_address + 1).hex()
        zpg_address = int(zpg_address, 16)
        zpg_value = self.read_memory(zpg_address, zpg_address + 1).hex()
        zpg_value = int(zpg_value, 16)

        ac = self.get_AC()
        ac = ac | zpg_value
        self.write_AC(ac)

        return "ORA", " zpg", zpg_address
    
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
        
        _, ac = self.check_negative(ac)
        self.check_zero(ac)
        self.registers[2:3] = ac.to_bytes(1, byteorder='big')

        return "ROL", "A"
    
    def rol_abs(self):
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
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)
        
        low, high, address = self.make_address(mem_address)
        value = self.read_memory(address, address + 1).hex()
        value = int(value, 16)

        ov = (value & (1 << 7)) >> 7
        value = value & ~(1 << 7)
        value = value << 1

        if self.carry_isSet():
            value = value | 1

        if ov == 0:
            self.clc()
        else:
            self.sec()

        _ , value = self.check_negative(value)
        self.check_zero(value)
        
        self.write_memory(address, value)
        
        return "ROL", " abs", low, high
    
    def rol_zpg(self):
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
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        zpg_address = self.read_memory(mem_address, mem_address + 1).hex()
        zpg_address = int(zpg_address, 16)
        zpg_value = self.read_memory(zpg_address, zpg_address + 1).hex()
        zpg_value = int(zpg_value, 16)

        ov = (zpg_value & (1 << 7)) >> 7
        zpg_value = zpg_value & ~(1 << 7)
        zpg_value = zpg_value << 1

        if self.carry_isSet():
            zpg_value = zpg_value | 1

        if ov == 0:
            self.clc()
        else:
            self.sec()

        _ , zpg_value = self.check_negative(zpg_value)
        self.check_zero(zpg_value)
        
        self.write_memory(zpg_address, zpg_value)
        
        return "ROL", " zpg", zpg_address

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

        _, ac = self.check_negative(ac)
        self.check_zero(ac)
        self.registers[2:3] = ac.to_bytes(1, byteorder='big')
        return "ROR", "A"
    
    def ror_abs(self):
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
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)
        
        low, high, address = self.make_address(mem_address)
        value = self.read_memory(address, address + 1).hex()
        value = int(value, 16)
        
        ov = value & 1
        value = value >> 1

        if self.carry_isSet():
            value = value | (1 << 7)
        else:
            value = value & ~(1 << 7)

        if ov == 0:
            self.unset_carry()
        else:
            self.set_carry()

        _, value = self.check_negative(value)
        self.check_zero(value)
        self.write_memory(address, value)
        
        return "ROR", " abs", low, high
    
    def ror_zpg(self):
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
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        zpg_address = self.read_memory(mem_address, mem_address + 1).hex()
        zpg_address = int(zpg_address, 16)
        zpg_value = self.read_memory(zpg_address, zpg_address + 1).hex()
        zpg_value = int(zpg_value, 16)
        
        ov = zpg_value & 1
        zpg_value = zpg_value >> 1

        if self.carry_isSet():
            zpg_value = zpg_value | (1 << 7)
        else:
            zpg_value = zpg_value & ~(1 << 7)

        if ov == 0:
            self.unset_carry()
        else:
            self.set_carry()

        _, zpg_value = self.check_negative(zpg_value)
        self.check_zero(zpg_value)
        self.write_memory(zpg_address, zpg_value)
        
        return "ROR", " zpg", zpg_address

    def rts(self):
        """RTS - Return from Subroutine
        
        The RTS instruction is used at the end of a subroutine to return to the calling routine. It pulls the program counter (minus one) from the stack.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        data = self.pop_from_stack(2)
        new_pc = bytearray(2)
        new_pc[0:1] = data[1:2]
        new_pc[1:2] = data[0:1]
        logger.debug("Going back to " + str(new_pc))
        
        logger.debug("Going back to " + str(new_pc))
        
        new_pc = int(new_pc.hex(), 16)
        self.write_PC(new_pc)
        
        return "RTS", "impl"

    def SBC(self, minuend: int, subtrahend: int) -> int:
        """Subtract two integers with carry and return result.
        
        Arguments:
            minuend {int} -- Starting number
            subtrahend {int} -- Number to be taken away
        
        Returns:
            int -- Difference
        """
        logging.debug("Subtracting with carry: " + str(minuend) + " and " + str(subtrahend))
        
        carry = ~1 if self.carry_isSet() else ~0
        difference = minuend + ~subtrahend - carry

        if difference >= -128 and difference <= 127:
            self.unset_overflow()
        elif difference < -128 or difference > 127:
            self.set_overflow()
            self.unset_carry()

        self.check_negative(difference)
        self.check_zero(difference)

        return difference
    
    def sbc_abs(self):
        """
        A,Z,C,N = A-M-(1-C)

        This instruction subtracts the contents of a memory location to the accumulator together with the not of the carry bit. If overflow occurs the carry bit is clear, this enables multiple byte subtraction to be performed.

        Processor Status after use:

        C	Carry Flag	Clear if overflow in bit 7
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Set if sign bit is incorrect
        N	Negative Flag	Set if bit 7 set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)
        
        low, high, address = self.make_address(mem_address)
        value = self.read_memory(address, address + 1)
        value = int(value, 16)
        ac = self.get_AC()
        
        ac = self.twos_complement(ac)
        two_value = self.twos_complement(value)

        diff = self.SBC(ac, two_value)
        self.write_AC(diff)

        return "SBC", " abs", low, high

    def sbc_imm(self):
        """
        A,Z,C,N = A-M-(1-C)

        This instruction subtracts the contents of a memory location to the accumulator together with the not of the carry bit. If overflow occurs the carry bit is clear, this enables multiple byte subtraction to be performed.

        Processor Status after use:

        C	Carry Flag	Clear if overflow in bit 7
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Set if sign bit is incorrect
        N	Negative Flag	Set if bit 7 set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        mem_value = self.read_memory(mem_address, mem_address + 1).hex()
        mem_value = int(mem_value, 16)
        ac = self.get_AC()

        ac = self.twos_complement(ac)
        two_value = self.twos_complement(mem_value)

        diff = self.SBC(ac, two_value)
        self.write_AC(diff)

        return "SBC", "   #", mem_value
    
    def sbc_zpg(self):
        """
        A,Z,C,N = A-M-(1-C)

        This instruction subtracts the contents of a memory location to the accumulator together with the not of the carry bit. If overflow occurs the carry bit is clear, this enables multiple byte subtraction to be performed.

        Processor Status after use:

        C	Carry Flag	Clear if overflow in bit 7
        Z	Zero Flag	Set if A = 0
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Set if sign bit is incorrect
        N	Negative Flag	Set if bit 7 set
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        address = self.read_memory(mem_address, mem_address + 1).hex()
        value = self.read_memory(address, address + 1)
        
        value = int(value, 16)
        ac = self.get_AC()
        ac = self.twos_complement(ac)
        two_value = self.twos_complement(value)

        diff = self.SBC(ac, two_value)
        self.write_AC(diff)

        return "SBC", " zpg", value

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
    
    def sta_abs(self):
        """
        STA - Store Accumulator

        M = A

        Stores the contents of the accumulator into memory.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)
        
        low, high, address = self.make_address(mem_address)

        ac = self.get_AC()
        self.write_memory(address, ac)

        return "STA", " abs", low, high
    
    def sta_zpg(self):
        """
        STA - Store Accumulator

        M = A

        Stores the contents of the accumulator into memory.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        zpg_address = self.read_memory(mem_address, mem_address + 1).hex()
        zpg_address = int(zpg_address, 16)

        ac = self.get_AC()

        self.write_memory(zpg_address, ac)

        return "STA", " zpg", zpg_address

    def stx_abs(self):
        """
        STX - Store X

        M = X

        Stores the contents of the X register into memory.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)
        
        low, high, address = self.make_address(mem_address)

        x = self.get_X()
        self.write_memory(address, x)

        return "STX", " abs", low, high

    def stx_zpg(self):
        """
        STX - Store X Register

        M = X

        Stores the contents of the X register into memory.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        zpg_address = self.read_memory(mem_address, mem_address + 1).hex()
        zpg_address = int(zpg_address, 16)

        x = self.get_X()

        self.write_memory(zpg_address, x)

        return "STX", " zpg", zpg_address
    
    def sty_abs(self):
        """
        STY - Store Y

        M = Y

        Stores the contents of the Y register into memory.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address+1)
        
        low, high, address = self.make_address(mem_address)

        y = self.get_Y()
        self.write_memory(address, y)

        return "STY", " abs", low, high

    def sty_zpg(self):
        """
        STY - Store X Register

        M = Y

        Stores the contents of the Y register into memory.

        Processor Status after use:

        C	Carry Flag	Not affected
        Z	Zero Flag	Not affected
        I	Interrupt Disable	Not affected
        D	Decimal Mode Flag	Not affected
        B	Break Command	Not affected
        V	Overflow Flag	Not affected
        N	Negative Flag	Not affected
        """
        mem_address = self.get_PC() + 1
        self.write_PC(mem_address)
        zpg_address = self.read_memory(mem_address, mem_address + 1).hex()
        zpg_address = int(zpg_address, 16)

        x = self.get_Y()

        self.write_memory(zpg_address, x)

        return "STY", " zpg", zpg_address

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
        self.check_negative_sign(sign)
        self.check_zero(ac)
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
        self.check_negative_sign(sign)
        self.check_zero(ac)
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
        self.check_negative_sign(sign)
        self.check_zero(sp)
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
        self.check_negative_sign(sign)
        self.check_zero(x)
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
        self.check_negative_sign(sign)
        self.check_zero(y)
        return "TYA", "impl"