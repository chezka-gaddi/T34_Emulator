import logging
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
            data = str.encode(data)
            checksum = line[-3:]

            self.memory[address:address+bytecount] = data[:]
            
            logger.debug(self.memory[address:address+bytecount])
            logger.debug(self.memory[address:address+1])

            logger.debug("Bytecount: " + str(bytecount))
            logger.debug("Address: " + str(address))
            logger.debug("Record Type: " + record_type)
            logger.debug(data)
            logger.debug(checksum)

        logger.debug(lineList)

    def start_emulator(self):
        command = input("> ")

        while command != "exit":
            if command[-1] == "R":
                self.run_program(command)
            command = input("> ")

    def run_program(self, address):
        print("Here")
