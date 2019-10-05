import unittest
import t34


class TestT34(unittest.TestCase):
    def setUp(self):
        self.emulator = t34.Emulator("test.txt")

    def test_load(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_memory_access(self):
        self.emulator.access_memory(200)


if __name__ == '__main__':
    unittest.main()
