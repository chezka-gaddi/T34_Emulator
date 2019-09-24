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

    #    with open(self.program) as f:
    #        lineList = f.readlines()

    #    lineList = [line.rstrip('\n') for line in open(self.program)]
        lineList = open(self.program, "rb").read()

        logger.debug(lineList)

    def start_emulator(self):
        command = input("> ")

        while command != "exit":
            if command[-1] == "R":
                self.run_program(command)
            command = input("> ")

    def run_program(self, address):
        print("Here")
