import os, sys
from core.parsing_functions import *

# -- REMOVE THIS IMPORT!!! --#
from debug_defs import *


class ExeFile:
    def __init__(self, path):
        self.path = path
        self.exc = False
        self.excInfo = ''
        if not os.path.exists(path):
            raise Exception('File is not found')
        if os.path.splitext(path)[-1] != '.exe':
            raise Exception('Wrong format of file. Please give exe format of file')

        self._parsefile()

    def _parsefile(self):
        with open(self.path, 'rb') as f:
            # DOS Header
            if f.read(2) != b'MZ':
                self.not_parsing('Broken file. No "MZ" in begin')
                return

            f.seek(60)
            pe_header = int.from_bytes(f.read(4), 'little')  # PE-Header address
            self.DOSProgram = f.read(pe_header - f.tell())  # Mini-Program for DOS
            del pe_header

            if f.read(4) != b'PE\0\0':
                self.not_parsing('Broken File. No "PE\\0\\0" in begin of PEHeader')
                return

            self.file_header = parse_file_header(f.read(20))
            optional_header_size = int.from_bytes(self.file_header['sizeOfOptionalHeader'][0], 'little')
            self.optional_header = parse_optional_header(f.read(optional_header_size))

            self.section_headers = parse_section_headers(f.read(int(self.file_header['numberOfSections'][1]) * 40))

            # TODO: see more parsing of exe files
            #   (for example https://habr.com/ru/post/266831/)

    def not_parsing(self, info):
        # Чтобы писать вместо двух строк одну с сообщением
        self.exc = 1
        self.excInfo = info

    @property
    def raw_data(self):
        """Return all data of file"""
        with open(self.path, 'rb') as f:
            yield f.read(1)

    def rva_to_raw(self):
        pass

    def raw_section_data(self, section_number):
        """Return RAW data of section with section_number (Numerating from 1)"""
        with open(self.path, 'rb') as f:
            if isinstance(section_number, int):
                section_number = self.section_name_by_number(section_number)

            section = self.section_headers[section_number]
            pointer = section['pointerToRawData']
            size = section['virtualSize']
            f.seek(pointer, 0)  # 0 - begin, 1 - current, 2 - end
            for _ in range(size):
                yield f.read(1)

    def section_name_by_number(self, section_number):
        names = list(self.section_headers.keys())
        return names[section_number - 1]
