import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
import core.exefile as x
from tests.baseTestClass import BaseTestClass


class TestOnFileQoobExe(BaseTestClass):
    path = 'examples/qoob.exe'

    def setUp(self):
        super().setUp()
        self.file = x.ExeFile(self.path)

    def test_rva_to_raw(self):
        expected = 0x6e00
        res = self.file.rva_to_raw(0x13000)

        self.assertEqual(expected, res[1])

    def test_rva_to_raw2(self):
        expected = 0x6e02
        res = self.file.rva_to_raw(0x13002)

        self.assertEqual(expected, res[1])

    def test_resources(self):
        expected = ('+ root\n| + ICON\n| | + 1\n| + RCDATA\n| | + 2\n| | + 8\n'
                    '| | + 10\n| | + 17\n| | + 18\n| | + 20\n| | + 21\n'
                    '| | + 30\n| | + 101\n| | + 102\n| | + 103\n| | + 104\n'
                    '| + GROUP_ICON\n| | + 1\n| + VERSION\n| | + 1')

        actual = str(self.file.resources())
        self.assertEqual(expected, actual)

    def test_no_export_table(self):
        actual = self.file.export_table()
        self.assertEqual('', str(actual))

    def test_relocations(self):
        actual = self.file.relocations()
        self.assertIsNone(actual)


class TestOnFileApp2Exe(BaseTestClass):
    path = 'examples/App2.exe'

    def setUp(self):
        super().setUp()
        self.file = x.ExeFile(self.path)

    def test_relocations(self):
        expected = ('BASE RELOCATIONS:\n	0x2000 RVA 12 SizeOfBlock 2 Count '
                    'of relocations\n		0x0006F4 HIGHLOW\n		0x000000 '
                    'ABSOULUTE')

        actual = self.file.relocations()
        self.assertEqual(expected, str(actual))

    def test_import_table(self):
        expected = ('Section contains the following imports:\n\n	'
                    'mscoree.dll\n	      0x26c7 Import Address Table\n	      '
                    '0x2000 Import Name Table\n	         '
                    '0x0 TimeDate Stamp\n	         0x0 Index of first '
                    'forwarder reference\n\n')
        actual = self.file.import_table()
        self.assertEqual(expected, str(actual))


class TestOnFileFirefox2Exe(BaseTestClass):
    path = 'examples/firefox2.exe'

    def setUp(self):
        super().setUp()
        self.file = x.ExeFile(self.path)

    def test_export_table(self):
        with open('tests/firefox2_expected/exportTable.txt') as f:
            expected = f.read()

        actual = self.file.export_table()

        self.assertEqual(expected, str(actual))


class TestCommonRaises(BaseTestClass):
    def test_file_not_found(self):
        path = 'WrongPath/nofile.exe'
        self.assertRaises(FileNotFoundError, lambda: x.ExeFile(path))

    def test_wrong_file_format(self):
        with self.assertRaises(ValueError) as excInfo:
            x.ExeFile('index.py')
        assert ('Wrong format of file. Please give exe/dll format of file' in
                str(excInfo.exception))

    def test_no_mz_signature(self):
        with self.assertRaises(x.BrokenFileError) as exc:
            x.ExeFile('examples/NoMZSignature.exe')
        assert 'Broken file. No "MZ" in begin' in str(exc.exception)

    def test_no_pe_signature(self):
        with self.assertRaises(x.BrokenFileError) as exc:
            x.ExeFile('examples/NoPESignature.exe')
        assert ('Broken File. No "PE\\0\\0" in begin of PEHeader'
                in str(exc.exception))


if __name__ == "__main__":
    unittest.main()
