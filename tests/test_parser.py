import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
import core.exefile as x


class TestProject(unittest.TestCase):
    path = '../examples/qoob.exe'

    def test_file_not_found(self):
        pass

    def test_rva_to_raw(self):
        file = x.ExeFile(TestProject.path)
        expected = 0x6e00
        res = file.rva_to_raw(0x13000)

        self.assertEqual(expected, res)

    def test_rva_to_raw2(self):
        file = x.ExeFile(TestProject.path)
        expected = 0x6e02
        res = file.rva_to_raw(0x13002)

        self.assertEqual(expected, res)


if __name__ == "__main__":
    unittest.main()
