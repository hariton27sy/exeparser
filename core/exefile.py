import os
import core.parsing_functions
from core.relocations import RelocationsParser

from core.resources import (ResourcesParser, ResourceInfo,
                            ResourceTable, GroupIcon)
from core.ImportTable import ImportTable
from core.exportTable import ExportTable


class BrokenFileError(Exception):
    def __init__(self, text):
        self.txt = text


class ExeFile:
    def __init__(self, path):
        self.path = path
        self.exc = False
        self.excInfo = ''
        if not os.path.exists(path):
            raise FileNotFoundError(f'File is not found {path}')
        if os.path.splitext(path)[-1] not in ('.exe', '.dll'):
            raise ValueError(
                'Wrong format of file. Please give exe/dll format of file')

        self._parsefile()

    def _parsefile(self):
        with open(self.path, 'rb') as f:
            # DOS Header
            if f.read(2) != b'MZ':
                raise BrokenFileError('Broken file. No "MZ" in begin')

            f.seek(60)
            pe_header = int.from_bytes(f.read(4),
                                       'little')  # PE-Header address
            self.DOSProgram = f.read(
                pe_header - f.tell())  # Mini-Program for DOS
            del pe_header

            if f.read(4) != b'PE\0\0':
                raise BrokenFileError(
                    'Broken File. No "PE\\0\\0" in begin of PEHeader')

            # Parse file and optional headers
            self.file_header = core.parsing_functions.parse_file_header(
                f.read(20))
            optional_header_size = int.from_bytes(
                self.file_header['sizeOfOptionalHeader'][0], 'little')
            self.optional_header = (core.parsing_functions.
                                    parse_optional_header(f.read(
                                        optional_header_size)))

            # Parse section headers
            self.section_headers = (core.parsing_functions.
                                    parse_section_headers(f.read(
                                        int(self.
                                            file_header['numberOfSections']
                                            [1]) * 40)))

    def raw_data(self):
        """Return all data of file"""
        with open(self.path, 'rb') as f:
            while f.readable():
                yield f.read(1)

    def rva_to_raw(self, rva):
        """Convert RVA to RAW

        rva - may be int or bytes object
        If it's bytes object it must be a little endian numbers"""
        if isinstance(rva, bytes):
            rva = int.from_bytes(rva, 'little')
        if not isinstance(rva, int):
            raise TypeError('rva may be only int or bytes object')

        alignment = int(self.optional_header['sectionAlignment'][1])

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

    def raw_section_data(self, section_number):
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
        return ExportTable(self)

    def import_table(self):
        return ImportTable(self)

    def resources(self):
        resource_position = int.from_bytes(
            self.optional_header['dataDirectory'][2][0],
            'little')
        if int.from_bytes(
                self.optional_header['dataDirectory'][2][1], 'little') == 0:
            return None
        with open(self.path, 'rb') as f:
            resource_position = self.rva_to_raw(resource_position)[1]
            return ResourcesParser(f, resource_position)

    def relocations(self):
        position = self.rva_to_raw(
            self.optional_header['dataDirectory'][5][0])[1]
        size = int.from_bytes(self.optional_header['dataDirectory'][5][1],
                              'little')
        if position == 0 or size == 0:
            return None
        return RelocationsParser(self.path, position, size)

    def get_summary(self):
        result = []
        section_alignment = int(self.optional_header['sectionAlignment'][1])
        for section in self.section_headers:
            size = int.from_bytes(section['virtualSize'], 'little')
            size = ((size // section_alignment +
                    1 if size % section_alignment > 0 else 0)
                    * section_alignment)
            result.append((section['name'], size))

        return result

    def get_resource(self, resources: ResourceTable,
                     resourceInfo: ResourceInfo):
        header = b""
        if resourceInfo.resourceType == "ICON":
            table = resources.get_element_by_name("GROUP_ICON")
            for e in table.elements:
                groupIcon = GroupIcon(self.get_resource(
                    resources, e.elements[0]))

                if resourceInfo.name in groupIcon.icons:
                    header = groupIcon.get_icon_header(resourceInfo.name)
                    break

        with open(self.path, 'rb') as f:
            raw = self.rva_to_raw(resourceInfo.rva)
            f.seek(raw[1])
            data = f.read(resourceInfo.size)
            if data[:4] == b"%PNG":
                header = b""
            return header + data
