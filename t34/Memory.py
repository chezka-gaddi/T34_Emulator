"""
.. module:: Memory
    :synopsis: Memory class that maintains the T34 memory.
"""

from typing import ByteString, TypeVar

Address = TypeVar("Address", bound=int)


class Memory:
    def __init__(self):
        """Initialize all of the Emulator's memory."""
        self.memory = bytearray(65536)
        self.registers = bytearray(7)
        self.initialize_registers()

    def initialize_registers(self):
        """
        Initialize registers to initial values.

        PC: 0
        AC: 0
        X: 0
        Y: 0
        SP: 0xFF
        SR: 0x20
        """
        self.registers = bytearray([0, 0, 0, 0, 0, 0, 0, 0])
        sp = int(self.registers[5:6].hex(), 16) | 255
        self.registers[5:6] = sp.to_bytes(1, byteorder='big')
        sr = ~int(self.registers[6:7].hex(), 16) & (1 << 5)
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')

    def read_memory(self, start: Address, end: Address):
        """
        Edits the contents of a specific memory address.

        :param str address: HEX address of the memory to be edited.
        :param str data: data to store into the memory address.
        """
        return self.memory[start:end]

    def write_memory(self, address: Address, data: ByteString):
        """
        Writes data to a specific memory address.

        :param Address address: HEX address of the memory to be edited.
        :param ByteString data: data to store into the memory address.
        """
        try:
            start = int(address, base=16)
        except:
            start = address
        try:
            self.memory[start:start+len(data)] = data
        except:
            data = data.to_bytes(1, byteorder='big')
            self.memory[start:start+len(data)] = data

    def write_PC(self, value: int):
        """Write to the PC register.

        Arguments:
            value {int} -- new PC
        """
        self.registers[0:2] = value.to_bytes(2, byteorder='big')

    def get_PC(self) -> int:
        """Retrieve current address stored in PC register.

        Returns:
            int -- address stored in PC
        """
        return int(self.registers[0:2].hex(), 16)

    def write_AC(self, value: int):
        """Write to the AC register.

        Arguments:
            value {int} -- new AC
        """
        self.check_zero(value)
        self.check_negative(value)
        self.registers[2:3] = value.to_bytes(1, byteorder='big')

    def get_AC(self) -> int:
        """Retrieve current address stored in AC register.

        Returns:
            int -- address stored in AC
        """
        return int(self.registers[2:3].hex(), 16)

    def write_X(self, value: int):
        """Write to the X register.

        Arguments:
            value {int} -- new X
        """
        self.check_zero(value)
        self.check_negative(value)
        self.registers[3:4] = value.to_bytes(1, byteorder='big')

    def get_X(self) -> int:
        """Retrieve current address stored in X register.

        Returns:
            int -- address stored in X
        """
        return int(self.registers[3:4].hex(), 16)

    def write_Y(self, value: int):
        """Write to the Y register.

        Arguments:
            value {int} -- new Y
        """
        self.check_zero(value)
        self.check_negative(value)
        self.registers[4:5] = value.to_bytes(1, byteorder='big')

    def get_Y(self) -> int:
        """Retrieve current address stored in Y register.

        Returns:
            int -- address stored in Y
        """
        return int(self.registers[4:5].hex(), 16)

    def write_SP(self, value: int):
        """Write to the SP register.

        Arguments:
            value {int} -- new SP
        """
        self.registers[5:6] = value.to_bytes(1, byteorder='big')

    def get_SP(self) -> int:
        """Retrieve current address stored in SP register.

        Returns:
            int -- address stored in SP
        """
        return int(self.registers[5:6].hex(), 16)

    def write_SR(self, value: int):
        """Write to the SR register.

        Arguments:
            value {int} -- new SR
        """
        self.registers[6:7] = value.to_bytes(1, byteorder='big')

    def get_SR(self) -> int:
        """Retrieve current address stored in SR register.

        Returns:
            int -- address stored in SR
        """
        return int(self.registers[6:7].hex(), 16)

    def check_carry(self, value: int) -> bool:
        if value > 256:
            self.set_carry()
            return True
        else:
            self.unset_carry()
            return False

    def set_carry(self):
        """Set carry bit to 1"""
        sr = int(self.registers[6:7].hex(), 16) | 1
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')

    def unset_carry(self):
        """Set carry bit to 0"""
        sr = int(self.registers[6:7].hex().upper(), 16) & ~1
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')

    def carry_isSet(self):
        """
        Checks if carry bit is set.

        Returns:
            Bool -- status of carry bit
        """
        sr = int(self.registers[6:7].hex(), 16)
        if sr & 1 == 1:
            return True
        else:
            return False
    
    def zero_isSet(self):
        """
        Checks if zero bit is set.

        Returns:
            Bool -- status of zero bit
        """
        sr = int(self.registers[6:7].hex(), 16)
        if (sr & (1 << 1)):
            return True
        else:
            return False
    
    def negative_isSet(self):
        """
        Checks if negative bit is set.

        Returns:
            Bool -- status of negative bit
        """
        sr = int(self.registers[6:7].hex(), 16)
        if (sr & (1 << 7)):
            return True
        else:
            return False
    
    def overflow_isSet(self):
        """
        Checks if overflow bit is set.

        Returns:
            Bool -- status of overflow bit
        """
        sr = int(self.registers[6:7].hex(), 16)
        if (sr & (1 << 6)):
            return True
        else:
            return False

    def check_negative_sign(self, sign: int):
        """
        Determines how to set the negative bit.

        Arguments:
            sign {int} -- sign of the number
        """
        if sign == 1:
            self.set_negative()
        else:
            self.unset_negative()

    def check_negative(self, value: int):
        """
        Checks sign of the value and sets the negative bit respectively.

        Arguments:
            value {int} -- value to check sign
        """
        sign = (value & (1 << 7)) >> 7
        if sign == 1:
            self.set_negative()
            return True
        else:
            self.unset_negative()
            return False

    def set_negative(self):
        """Set negative bit to 1"""
        sr = int(self.registers[6:7].hex().upper(), 16) | (1 << 7)
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')

    def unset_negative(self):
        """Set negative bit to 0"""
        sr = int(self.registers[6:7].hex().upper(), 16) & ~(1 << 7)
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')

    def check_zero(self, value: int):
        """
        Checks is the value is zero and sets the zero bit respectively.

        Arguments:
            value {int} -- value to check
        """
        if value == 0:
            self.set_zero()
        else:
            self.unset_zero()

    def set_zero(self):
        """Set zero bit to 1"""
        sr = int(self.registers[6:7].hex().upper(), 16) | 2
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')

    def unset_zero(self):
        """Unset zero bit"""
        sr = int(self.registers[6:7].hex().upper(), 16) & ~2
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')

    def set_overflow(self):
        """Set overflow bit"""
        sr = int(self.registers[6:7].hex(), 16) | 64
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')

    def unset_overflow(self):
        """Unset overflow bit"""
        sr = int(self.registers[6:7].hex(), 16) & ~64
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')
