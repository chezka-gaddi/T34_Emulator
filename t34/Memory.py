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
        self.registers = bytearray(8)
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

        :param str address: HEX address of the memory to be edited.
        :param str data: data to store into the memory address.
        """
        start = int(address, base=16)
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
        self.registers[2:3] = value.to_bytes(1, byteorder='big')

    def get_AC(self) -> int:
        """Retrieve current address stored in AC register.

        Returns:
            int -- address stored in AC
        """
        return int(self.registers[2:3].hex(), 16)

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
        if value < 0 or value > 127:
            self.set_negative()
        else:
            self.unset_negative()

    def set_negative(self):
        """Set negative bit to 1"""
        sr = int(self.registers[6:7].hex().upper(), 16) | (1 << 7)
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')

    def unset_negative(self):
        """Set negative bit to 1"""
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
