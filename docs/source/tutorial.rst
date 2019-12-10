T34 Emulator Tutorial
=====================

This is the tutorial on how to use the T34 Emulator module.

Overview
********

The T34 Emulator has been implemented up to the absolute addressing modes.


Running the Application
***********************


Functionality
*************
The monitor will have similar functionality as an OS. The T34 monitor has six functions;

1. :ref:`Load a Program`

2. :ref:`Display the content of a specific memory address`

3. :ref:`Display the content of a range of memory addresses`

4. :ref:`Edit memory locations`

5. :ref:`Run program starting as a specified address`

6. :ref:`Exit the program`


.. _Load a Program:

Load a Program
**************
The machine can start in two modes. Either the user provided an object file (a program), if so,
the program is loaded into the correct memory location, or the user just starts the emulator
without any program. In both cases the monitor is started, and the user is provided with the
monitor prompt (>).

To start the application with a program, run the application with the name of the object file.

.. code-block:: bash

    $ python3 t34.py [filename]


.. _Display the content of a specific memory address:

Display the content of a specific memory address
************************************************

By typing in the memory address in HEX at the Monitor prompt, the Monitor returns the byte (in
HEX format) at that location.

.. code-block:: console

    > 200
     200    A9


.. _Display the content of a range of memory addresses:

Display the content of a range of memory addresses
**************************************************

By typing in the starting address in HEX, followed by a period and finally the ending address in
HEX at the Monitor prompt, the Monitor returns the bytes between those locations.

.. code-block:: console

        > 200.20F
         200    A9 00 85 00 A5 00 8D 00
         208    80 E6 00 4C 04 02 00 00


.. _Edit memory locations:

Edit memory locations
*********************

By typing in the starting address in HEX, followed by a colon, and then the new values for the
memory locations at the Monitor prompt, the monitor updates the current locations.


.. code-block:: console

        > 300: A9 04 85 07 A0 00 84 06 A9 A0 91 06 C8 D0 FB E6 07
        > 300.310
         300    A9 04 85 07 A0 00 84 06
         308    A9 A0 91 06 C8 D0 FB E6
         310    07


.. _Run program starting as a specified address:

Run program starting as a specified address
*******************************************

By typing in the starting address in HEX, followed by an R at the Monitor prompt. The monitor
will execute all code starting at the address and up until the first BRK (opcode 00).

.. code-block:: console

    > 200R
     PC  OPC  INS   AMOD OPRND  AC XR YR SP NV-BDIZC
     200

.. _Exit the program:

Exit the program
****************

The user should be able to exit the monitor (and python) in three ways:

1. Ctrl-C (keyboard interrupt)

2. Ctrl-D (EOF)

3. Type exit at the monitor prompt ( > exit)