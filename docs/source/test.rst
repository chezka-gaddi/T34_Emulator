Testing the Program
===================

:class:`Emulator` is fully tested!

.. autoclass:: t34.TestEmulator
    :members:

Accessing Memory
****************

.. testsetup:: *

    import Emulator

    emulator = Emulator("test.txt")

.. doctest::

    >>> emulator.access_memory("200")
     200    A9


Accessing Memory Range
**********************

.. doctest::

    >>> emulator.access_memory_range("200","20F")
     200    A9 00 85 00 A5 00 8D 00
     208    80 E6 00 4C 04 02 00 00


Editing Memory Locations
************************

.. doctest::

    >>> 300: A9 04 85 07 A0 00 84 06 A9 A0 91 06 C8 D0 FB E6 07
    >>> 300.310
     300    A9 04 85 07 A0 00 84 06
     308    A9 A0 91 06 C8 D0 FB E6
     310    07

