import os, sys
from core.parsing_functions import *
from core.tables_parsers import *


class ExeFile:
    def __init__(self, path):
        self.path = path
        self.exc = False
        self.excInfo = ''
        if not os.path.exists(path):
            raise Exception('File is not found')
        if os.path.splitext(path)[-1] not in ('.exe', '.dll'):
            raise Exception(
                'Wrong format of file. Please give exe format of file')

        self._parsefile()
        import_index = self.rva_to_raw(int.from_bytes(
            self.optional_header['dataDirectory'][1][0], 'little'))[0]
        self.import_table = parse_import_table(import_index)

    def _parsefile(self):
        with open(self.path, 'rb') as f:
            # DOS Header
            if f.read(2) != b'MZ':
                self.not_parsing('Broken file. No "MZ" in begin')
                return

            f.seek(60)
            pe_header = int.from_bytes(f.read(4),
                                       'little')  # PE-Header address
            self.DOSProgram = f.read(
                pe_header - f.tell())  # Mini-Program for DOS
            del pe_header

            if f.read(4) != b'PE\0\0':
                self.not_parsing(
                    'Broken File. No "PE\\0\\0" in begin of PEHeader')
                return

            self.file_header = parse_file_header(f.read(20))
            optional_header_size = int.from_bytes(
                self.file_header['sizeOfOptionalHeader'][0], 'little')
            self.optional_header = parse_optional_header(
                f.read(optional_header_size))

            self.section_headers = parse_section_headers(
                f.read(int(self.file_header['numberOfSections'][1]) * 40))

            # TODO: see more parsing of exe files
            #   (for example https://habr.com/ru/post/266831/)
            #   It is here while project is not passed

    def not_parsing(self, info):
        # Чтобы писать вместо двух строк одну с сообщением
        self.exc = 1
        self.excInfo = info

    @property
    def raw_data(self):
        """Return all data of file"""
        with open(self.path, 'rb') as f:
            yield f.read(1)

    def rva_to_raw(self, rva: int):
        """Convert RVA to RAW

        rva - may be int or bytes object"""
        if isinstance(rva, bytes):
            rva = int.from_bytes(rva, 'little')
        if not isinstance(rva, int):
            raise TypeError('rva may be only int or bytes object')

        alignment = int(self.optional_header['sectionAlignment'][1])
        print(alignment)

        def find_section(rva):
            for i in range(int(self.file_header['numberOfSections'][1])):
                start = int.from_bytes(
                    self.section_headers[i]['virtualAddress'], 'little')
                end = start + int.from_bytes(
                    self.section_headers[i]['virtualSize'], 'little')
                if start <= rva < end:
                    return i
            return -1

        indexSection = find_section(rva)
        if indexSection != -1:
            return (indexSection,
                    int.from_bytes(self.section_headers[indexSection]
                                   ['pointerToRawData'], 'little') + rva -
                    int.from_bytes(self.section_headers[indexSection]
                                   ['virtualAddress'], "little"))

        return indexSection, rva

    def raw_section_data(self, section_number, ):
        """Return RAW data of section with
        section_number (Numerating from 1)"""
        with open(self.path, 'rb') as f:
            section = self.section_headers[section_number - 1]
            pointer = section['pointerToRawData']
            size = section['virtualSize']
            f.seek(int.from_bytes(pointer, 'little'), 0)  # 0 - begin,
            # 1 - current,
            # 2 - end
            for _ in range(int.from_bytes(size, 'little')):
                yield f.read(1)

    def export_table(self):
        return parse_export_table(self)

    def parse_import_table(self):
        return parse_import_table(self)
