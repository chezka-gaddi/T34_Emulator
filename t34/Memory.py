class Memory:
    def __init__(self):
        self.memory = bytearray(65536)
        self.registers = bytearray(8)
        self.initialize_registers()

    def initialize_registers(self):
        self.registers = bytearray([0, 0, 0, 0, 0, 0, 0, 0])
        sp = int(self.registers[5:6].hex(), 16) | 255
        self.registers[5:6] = sp.to_bytes(1, byteorder='big')
        sr = ~int(self.registers[6:7].hex(), 16) & (1 << 5)
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')

    def read_memory(self, start, end):
        """
        Edits the contents of a specific memory address.

        :param str address: HEX address of the memory to be edited.
        :param str data: data to store into the memory address.
        """
        return self.memory[start:end]

    def write_memory(self, address, data):
        """
        Writes data to a specific memory address.

        :param str address: HEX address of the memory to be edited.
        :param str data: data to store into the memory address.
        """
        self.memory[int(address, 16):] = data[:]
