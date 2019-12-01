import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
import common_funcs


class TestBytesLineToSymbols(unittest.TestCase):
    def test_bytes_line_to_symbols(self):
        test_line = '55 89 E5 83 EC 18 89 5D'
        expected = 'U......]'
        self.equal(test_line, expected)

    def test_OnNone(self):
        test_line = None
        self.equal(test_line, '')

    def test_pairs_hex_line(self):
        test_line = '8955 83E5 18EC 5D89'
        expected = 'U......]'
        self.equal(test_line, expected)

    def equal(self, test_line, expected):
        result = common_funcs.bytes_line_to_symbols(test_line)
        self.assertEqual(expected, result)


class TestHexFromBytes(unittest.TestCase):
    def test_OnEmptyString(self):
        expected = ""
        actual = common_funcs.hex_from_bytes(b"")

        self.assertEqual(expected, actual)

    def test_ThrowsOnWrongDataTypes(self):
        with self.assertRaises(TypeError):
            common_funcs.hex_from_bytes(123)

    def test_OnCommonData(self):
        expected = '0x0ABB'
        actual = common_funcs.hex_from_bytes(b'\xBB\x0A')
        self.assertEqual(expected, actual)


class TestFormattedOutput(unittest.TestCase):
    def test_CommonData(self):
        line = [0x55, 0x89, 0xE5, 0x83, 0xEC, 0x18, 0x89, 0x5D, 63, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 126]
        actual = ''.join(common_funcs.formatted_output(0, line))

        expected = "0x00000000: 55 89 E5 83 EC 18 89 5D 3F 00 00 00 00 " \
                   "00 00 00  U......]?.......\n0x00000010: 00 00 00 00 " \
                   "00 00 00 7E                          .......~\n"

        self.assertEqual(expected, actual)

    def test_OnEmptyString(self):
        actual = ''.join(common_funcs.formatted_output(0, ""))
        expected = ''

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
