class Memory:
    def __init__(self):
        self.memory = bytearray(65536)
        self.registers = bytearray(8)
        sp = int(self.registers[5:6].hex(), 16) | 255
        self.registers[5:6] = sp.to_bytes(1, byteorder='big')
        sr = ~int(self.registers[6:7].hex(), 16) & (1 << 5)
        self.registers[6:7] = sr.to_bytes(1, byteorder='big')

    def edit(self, address, data):
        """
        Edits the contents of a specific memory address.

        :param str address: HEX address of the memory to be edited.
        :param str data: data to store into the memory address.
        """
        data = [int(byte, base=16) for byte in data.split()]

        self.memory[address:] = data[:]

    def get_memory(self, address):
        return self.memory[address:address+1].hex().upper()
