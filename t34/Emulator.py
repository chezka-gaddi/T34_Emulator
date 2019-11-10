"""
.. module:: Emulator
    :synopsis: Emulator class that runs the T34 Emulator
"""
import logging
import math
import string
logger = logging.getLogger(__name__)


class Emulator:
    """Class to store an emulator and runs program files."""

    def __init__(self, program_name=None):
        """
        Creates an emulator and sets up the memory space for the main memory and the registers.

        :param program_name: name of the program file to be run
        :type program_name: string
        """
        self.memory = bytearray(65536)
        self.registers = bytearray(8)
        self.program = program_name
        if self.program is not None:
            self.load_program()

    def load_program(self):
        """
        Loads the program.

        :return: successful read
        :rtype: bool
        """
        with open(self.program) as f:
            lineList = f.readlines()

        for line in lineList:
            logger.debug(line)
            bytecount = line[1:3]
            bytecount = int(bytecount, 16)
            address = line[3:7]
            address = int(address, 16)
            record_type = line[7:9]
            data = line[9:-3]
            # data = str.encode(data)
            checksum = line[-3:]

            data = [int(data[i:i+2], 16) for i in range(0, len(data), 2)]

            self.memory[address:address+bytecount] = data[:]

            logger.debug(self.memory[address:address+bytecount])
            logger.debug(self.memory[address:address+1])

            logger.debug("Address: " + str(address))
            logger.debug("Record Type: " + record_type)
            logger.debug(data)
            logger.debug(checksum)

        logger.debug(lineList)

    def start_emulator(self):
        """Starts the emulator and evaluates and executes commands."""
        command = input("> ")

        while command != "exit":
            pidx = command.find('.')
            cidx = command.find(":")

            # Run program
            if command.endswith("R"):
                output = self.run_program(command[:-1])
                print(output)

            # Access memory range
            elif pidx != -1:
                output = self.access_memory_range(
                    command[:pidx], command[pidx+1:])
                print(output)

            # Edit memory
            elif cidx != -1:
                self.edit_memory(command[:cidx], command[cidx+1:])

            # Access memory address
            else:
                output = self.access_memory(command)
                print(output)

            command = input("> ")

    def access_memory(self, address):
        """
        Accesses the memory address and displays the contents.

        :param str address: HEX address of the memory to be accessed.

        :return: memory content
        :rtype: string
        """
        logger.debug("Accessing Memory")

        ad = int(address, 16)
        return str(address) + "\t" + str(self.memory[ad:ad+1].hex().upper())

    def access_memory_range(self, begin, end):
        """
        Accesses a memory range and displays all the contents.

        :param str begin: beginning HEX address of the memory to be accessed.
        :param str end: end HEX address of the memory to be accessed.

        :return out: contents of the memory range.
        :rtype: string
        """
        logger.debug("Accessing memory range")

        b = int(begin, 16)
        e = int(end, 16)
        idx = e-b+1
        out = ""

        s = b
        i = 0
        while s <= e:
            f = s+8 if s+8 <= e else e+1
            data = self.memory[s:f]
            data = " ".join(["{:02x}".format(x).upper() for x in data])
            out += hex(s).lstrip("0x") or "0" + "\t" + str(data) + "\n"
            i += 1
            s = b + i*8
        return out

    def edit_memory(self, address, data):
        """
        Edits the contents of a specific memory address.

        :param str address: HEX address of the memory to be edited.
        :param str data: data to store into the memory address.
        """
        logger.debug(data)
        data = [int(byte, base=16) for byte in data.split()]
        # data = [int(data[i:i+2], 16) for i in range(0, len(data), 2)]
        logger.debug(data)

        self.memory[int(address, 16):] = data[:]

    def run_program(self, address):
        """
        Runs and executes the program. It also prints out the contents of the registers.

        :param address: Location of the command to be executed.
        :return output: Contents of all the registers.
        :rtype: string
        """
        ad = int(address)
        self.registers[0] = ad
        output = " PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC\n"

        output += str(self.registers[0])
        return output
