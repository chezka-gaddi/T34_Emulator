Testing the Program
===================

All of the functionality of the :class:`Emulator` class is tested with the unittest found in the TestEmulator and TestInstruction and TestMemory modules. All tests could be run with the command

.. code-block:: console

    nosetests --verbosity=2 --rednose ./

Test Emulator
*************

.. automodule:: tests.test_emulator
    :members:

Test Memory
***********

.. automodule:: tests.test_memory
    :members:

Test Instructions
*****************

.. automodule:: tests.test_instructions
    :members:

Immediate Instructions
----------------------

.. automodule:: tests.test_instructions_immediate
    :members:

Zeropage Instructions
---------------------

.. automodule:: tests.test_instructions_zeropage
    :members:

Relative Instructions
---------------------

.. automodule:: tests.test_instructions_relative
    :members:

Absolute Instructions
---------------------

.. automodule:: tests.test_instructions_absolute
    :members: