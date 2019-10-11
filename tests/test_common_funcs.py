import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
import common_funcs


class TestCommonFunc(unittest.TestCase):
    def test_bytes_line_to_symbols(self):
        test_line = '55 89 E5 83 EC 18 89 5D'
        expected = 'U......]'
        self.equal(test_line, expected)

    def test_pairs_hex_line(self):
        test_line = '8955 83E5 18EC 5D89'
        expected = 'U......]'
        self.equal(test_line, expected)

    def equal(self, test_line, expected):
        result = common_funcs.bytes_line_to_symbols(test_line)
        self.assertEqual(expected, result)

    def test_formatted_output(self):
        line = [0x55, 0x89, 0xE5, 0x83, 0xEC, 0x18, 0x89, 0x5D, 63, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 126]
        result = common_funcs.formatted_output(0, line)
        print()
        print(result)


if __name__ == "__main__":
    unittest.main()
