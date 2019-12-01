import struct


RESOURCE_TYPES = {
    1: "CURSOR",
    2: "BITMAP",
    3: "ICON",
    4: "MENU",
    5: "DIALOG",
    6: "STRING",
    7: "FONTDIR",
    8: "FONT",
    9: "ACCELERATORS",
    10: "RCDATA",
    11: "MESSAGETABLE",
    12: "GROUP_CURSOR",
    14: "GROUP_ICON",
    16: "VERSION",
    24: "MANIFEST",
    0x2000: "NEWRESOURCE",
    0x7fff: "ERROR"
}
HALF_MAX_INT = 0xffffffff // 2


class ResourceTable:
    def __init__(self, idOrName, characteristics, timeDateStamp, version):
        self.type = 0
        self.name = idOrName
        self.characteristics = characteristics
        self.timeDateStamp = timeDateStamp
        self.version = version
        self.elements = []


class ResourceInfo:
    def __init__(self, name, rva, size, codePage):
        self.type = 1
        self.name = name
        self.rva = rva
        self.size = size
        self.codePage = codePage


class ResourcesParser:
    def __init__(self, fileStream, start_position=-1):
        temp_position = fileStream.tell()
        if start_position != -1:
            fileStream.seek(start_position)
        self.f = fileStream
        self.start_position = fileStream.tell()
        self.table = self.get_table('root')
        self.f.seek(temp_position)

    def get_table(self, name, position=0, level=0):
        temp_position = self.f.tell()
        self.f.seek(self.start_position + position)
        info = struct.unpack('IIHHHH', self.f.read(16))
        table = ResourceTable(name,
                              info[0],
                              info[1],
                              f'{info[2]}.{info[3]}')
        for i in range(info[4]):
            name, elementOffset = struct.unpack('II', self.f.read(8))
            name = self.get_directory_string(name)
            table.elements.append(self.add_element(level, name, elementOffset))
        for i in range(info[5]):
            name, elementOffset = struct.unpack('II', self.f.read(8))
            if level == 0 and name in RESOURCE_TYPES:
                name = RESOURCE_TYPES[name]
            table.elements.append(self.add_element(level, name, elementOffset))
        self.f.seek(temp_position)

        return table

    def get_directory_string(self, position):
        temp_position = self.f.tell()
        self.f.seek(position + self.start_position)
        length = int.from_bytes(self.f.read(2), 'little')
        result = self.f.read(length).decode('utf-8')
        self.f.seek(temp_position)
        return result

    def get_resource_info(self, name, position):
        tempPosition = self.f.tell()
        self.f.seek(self.start_position + position)
        rva, size, codePage = struct.unpack('III', self.f.read(12))
        result = ResourceInfo(name, rva, size, codePage)
        self.f.seek(tempPosition)
        return result

    def add_element(self, level, name, elementOffset):
        if elementOffset > HALF_MAX_INT:
            elementOffset -= HALF_MAX_INT + 1
            return self.get_table(name, elementOffset, level + 1)
        else:
            return self.get_resource_info(name, elementOffset)

    def get_cli_string(self, padding="", element=None):
        if element is None:
            element = self.table
        if element.type == 1:
            return f"{padding}{element.name}"
        result = [f"{padding}+ {element.name}"]
        for e in element.elements:
            if e.type == 0:
                result.append(self.get_cli_string(f"{padding}| ", e))

        return "\n".join(result)

    def __str__(self):
        return self.get_cli_string()
