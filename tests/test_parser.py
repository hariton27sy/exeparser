import os
import sys
import unittest
PARENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          os.path.pardir)
sys.path.append(PARENT_DIR)
import core.exefile as x


def full_path(path):
    return os.path.join(PARENT_DIR, path)


class TestOnFileQoobExe(unittest.TestCase):
    path = 'examples/qoob.exe'

    def setUp(self):
        self.file = x.ExeFile(full_path(self.path))

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

    def test_raw_section_header(self):
        expected = (b'<\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                    b'\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00'
                    b'\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00'
                    b'\x00\x00\x00\x00\x00\x00\x00|p@\x00\x00\x00\x00\x00\x00'
                    b'\x00\x00\x00\x00\x00\x00\x00')
        actual = b"".join(self.file.raw_section_data(2))

        self.assertEqual(expected, actual)


class TestOnFileApp2Exe(unittest.TestCase):
    path = 'examples/App2.exe'

    def setUp(self):
        self.file = x.ExeFile(full_path(self.path))

    def test_relocations(self):
        expected = ('BASE RELOCATIONS:\n	0x2000 RVA 12 SizeOfBlock 2 Count '
                    'of relocations\n		0x0006F4 HIGHLOW\n		0x000000 '
                    'ABSOULUTE')

        actual = self.file.relocations()
        self.assertEqual(expected, str(actual))

    def test_import_table(self):
        expected = {
            'originalFirstThunk': 9927,
            'timeDateStamp': 0,
            'forwarderChain': 0,
            'name': "mscoree.dll",
            'firstThunk': 8192
        }
        actual = self.file.import_table()

        self.assertEqual(1, len(actual.table))
        for field in expected:
            self.assertEqual(expected[field], actual.table[0][field])
        self.assertEqual(1, len(actual.table[0]['functions']))

    def test_resources(self):
        expected = """+ root\n| + VERSION\n| | + 1\n| + MANIFEST\n| | + 1"""

        actual = self.file.resources()
        self.assertEqual(expected, str(actual))


class TestOnFileFirefox2Exe(unittest.TestCase):
    path = 'examples/firefox2.exe'

    def setUp(self):
        self.file = x.ExeFile(full_path(self.path))

    def test_data_directory(self):
        expected = [(b'\x05\x04\x04\x00', b'\xcf\x07\x00\x00'),
                    (b'\xd4\x0b\x04\x00', b'h\x01\x00\x00'),
                    (b'\x00\x80\x04\x00', b'\xb0%\x03\x00'),
                    (b'\x00\x00\x00\x00', b'\x00\x00\x00\x00'),
                    (b'\x00\x80\x07\x00', b' \x1e\x00\x00'),
                    (b'\x00\xb0\x07\x00', b"p'\x00\x00"),
                    (b'j\xfb\x03\x00', b'\x1c\x00\x00\x00'),
                    (b'\x00\x00\x00\x00', b'\x00\x00\x00\x00'),
                    (b'\x00\x00\x00\x00', b'\x00\x00\x00\x00'),
                    (b'\xd4\xcc\x03\x00', b'\x18\x00\x00\x00'),
                    (b'\xb8\xb0\x03\x00', b'\xa0\x00\x00\x00'),
                    (b'\x00\x00\x00\x00', b'\x00\x00\x00\x00'),
                    (b'\x8c\x12\x04\x00', b'P\x05\x00\x00'),
                    (b'\xa4\x00\x04\x00', b'\xe0\x00\x00\x00'),
                    (b'\x00\x00\x00\x00', b'\x00\x00\x00\x00'),
                    (b'\x00\x00\x00\x00', b'\x00\x00\x00\x00')]

        actual = self.file.optional_header['dataDirectory']
        self.assertEqual(16, len(actual))
        self.assertEqual(expected, actual)

    def test_export_table(self):
        with open(full_path('tests/firefox2_expected/exportTable.txt')) as f:
            expected = f.read()

        actual = self.file.export_table()

        self.assertEqual(expected, str(actual))

    def test_dependents(self):
        expected = {
            "ADVAPI32.dll",
            "KERNEL32.dll",
            "MSVCP140.dll",
            "VCRUNTIME140.dll",
            "api-ms-win-crt-convert-l1-1-0.dll",
            "api-ms-win-crt-environment-l1-1-0.dll",
            "api-ms-win-crt-filesystem-l1-1-0.dll",
            "api-ms-win-crt-heap-l1-1-0.dll",
            "api-ms-win-crt-locale-l1-1-0.dll",
            "api-ms-win-crt-math-l1-1-0.dll",
            "api-ms-win-crt-runtime-l1-1-0.dll",
            "api-ms-win-crt-stdio-l1-1-0.dll",
            "api-ms-win-crt-string-l1-1-0.dll",
            "api-ms-win-crt-time-l1-1-0.dll",
            "api-ms-win-crt-utility-l1-1-0.dll",
            "mozglue.dll",
            "ntdll.dll"
        }

        actual = self.file.import_table().get_dependencies()
        self.assertEqual(expected, set(actual))

        # That no repeats
        self.assertEqual(len(set(actual)), len(actual))

    def test_get_when_resource_is_png(self):
        resources = self.file.resources()
        resource = resources.table.elements[0].elements[11].elements[0]

        actual = self.file.get_resource(resource)
        self.assertEqual(b"\x89PNG", actual[:4])


class TestCommonRaises(unittest.TestCase):
    def test_file_not_found(self):
        self.assertRaises(FileNotFoundError, lambda: x.ExeFile(
            full_path('WrongPath/nofile.exe')))

    def test_wrong_file_format(self):
        with self.assertRaises(x.BrokenFileError) as excInfo:
            x.ExeFile(full_path('index.py'))
        self.assertIn('Broken file. No "MZ" in begin', str(excInfo.exception))

    def test_no_mz_signature(self):
        with self.assertRaises(x.BrokenFileError) as exc:
            x.ExeFile(full_path('examples/NoMZSignature.exe'))
        self.assertIn('Broken file. No "MZ" in begin', str(exc.exception))

    def test_no_pe_signature(self):
        with self.assertRaises(x.BrokenFileError) as exc:
            x.ExeFile(full_path('examples/NoPESignature.exe'))
        self.assertIn('Broken File. No "PE\\0\\0" in begin of PEHeader',
                      str(exc.exception))


if __name__ == "__main__":
    unittest.main()
