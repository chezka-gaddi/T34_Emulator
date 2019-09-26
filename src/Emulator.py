import logging
import math
import string
logger = logging.getLogger(__name__)


class Emulator:
    def __init__(self, program_name=None):
        """
            **Constructor**

            Creates an emulator.

            Parameters
            ----------
            program_name
                Name of the program to be loaded into the emulator
        """
        self.memory = bytearray(65536)
        self.program = program_name
        if self.program is not None:
            self.load_program()

    def load_program(self):
        """
            **Load Program**

            This function loads the program.

            :return: successful read

            - Example::
                load_program(a.c)

            - Expected Success Response::
                True

            - Expected Fail Response::
                False

        """

        with open(self.program) as f:
            lineList = f.readlines()

        # lineList = [line.rstrip('\n') for line in open(self.program)]
        # lineList = open(self.program, "rb").read()

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
        """
        """

        command = input("> ")

        while command != "exit":
            pidx = command.find('.')
            cidx = command.find(":")

            if command[-1] == "R":
                self.run_program(command)

            elif pidx != -1:
                self.access_memory_range(command[:pidx], command[pidx+1:])
            elif cidx != -1:
                self.edit_memory(command[:cidx], command[cidx+1:])

            else:
                self.access_memory(command)
            command = input("> ")

    def access_memory(self, address):
        """
        """

        ad = int(address, 16)
        print(address, self.memory[ad:ad+1].hex().upper())

    def access_memory_range(self, begin, end):
        """
        """

        b = int(begin, 16)
        e = int(end, 16)
        idx = math.ceil((e - b)/8)
        logger.debug(idx)
        i = 0
        while i < idx:
            s = b + i*8
            f = s+8 if s+8 < e else e+1
            data = self.memory[s:f]
            data = " ".join(["{:02x}".format(x).upper() for x in data])
            print(hex(s).lstrip("0x"), data)
            i += 1

    def edit_memory(self, address, data):
        data = data.translate({ord(c): None for c in string.whitespace})
        logger.debug(data)
        data = [int(data[i:i+2], 16) for i in range(0, len(data), 2)]
        logger.debug(data)

        self.memory[int(address, 16):] = data[:]

    def run_program(self, address):
        print("Here")
