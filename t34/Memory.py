class Memory:
    def __init__(self):
        self.memory = bytearray(65536)
        self.registers = bytearray(8)

    def get_memory(self, address):
        return self.memory[address:address+1].hex().upper()
