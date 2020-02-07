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
    def __init__(self, idOrName, characteristics,
                 timeDateStamp, version, resourceType=None):
        self.type = 0
        self.name = idOrName
        self.characteristics = characteristics
        self.timeDateStamp = timeDateStamp
        self.version = version
        self.elements = []
        self.resourceType = resourceType

    def get_element_by_name(self, name):
        counter = 0
        while (counter < len(self.elements) and
               self.elements[counter].name != name):
            counter += 1
        return self.elements[counter] if counter < len(self.elements) else None


class ResourceInfo:
    def __init__(self, name, rva, size, codePage, resourceType=None):
        self.type = 1
        self.resourceType = resourceType
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

    def get_table(self, name, position=0, level=0, resourceType=None):
        temp_position = self.f.tell()
        self.f.seek(self.start_position + position)
        info = struct.unpack('IIHHHH', self.f.read(16))
        table = ResourceTable(name,
                              info[0],
                              info[1],
                              f'{info[2]}.{info[3]}', resourceType)
        for i in range(info[4]):
            name, elementOffset = struct.unpack('II', self.f.read(8))
            name = self.get_directory_string(name - HALF_MAX_INT - 1)
            table.elements.append(self.add_element(level, name,
                                                   table.name, elementOffset,
                                                   resourceType))
        for i in range(info[5]):
            name, elementOffset = struct.unpack('II', self.f.read(8))
            if level == 0 and name in RESOURCE_TYPES:
                name = RESOURCE_TYPES[name]
                resourceType = name
            table.elements.append(self.add_element(
                level, name, table.name, elementOffset, resourceType))
        self.f.seek(temp_position)

        return table

    def get_directory_string(self, position):
        temp_position = self.f.tell()
        self.f.seek(position + self.start_position)
        length = int.from_bytes(self.f.read(2), 'little')
        result = self.f.read(length * 2).decode('utf-16')
        self.f.seek(temp_position)
        return result

    def get_resource_info(self, name, position, resourceType=None):
        tempPosition = self.f.tell()
        self.f.seek(self.start_position + position)
        rva, size, codePage = struct.unpack('III', self.f.read(12))
        result = ResourceInfo(name, rva, size, codePage, resourceType)
        self.f.seek(tempPosition)
        return result

    def add_element(self, level, name, parentName,
                    elementOffset, resourceType=None):
        if elementOffset > HALF_MAX_INT:
            elementOffset -= HALF_MAX_INT + 1
            return self.get_table(name, elementOffset, level + 1, resourceType)
        else:
            return self.get_resource_info(parentName,
                                          elementOffset, resourceType)

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


class GroupIcon:
    def __init__(self, data: bytes):
        self.type, self.count = struct.unpack("HH", data[2:6])
        self.mainHeader = data[:4] + b'\x01\x00'
        self.icons = {}
        for i in range(self.count):
            icon_info = struct.unpack("BBBBHHIH", data[6 + i * 14:20 + i * 14])
            self.icons[icon_info[-1]] = data[6 + i * 14:20 + i * 14]

    def get_icon_header(self, iconId):
        if iconId in self.icons:
            return (self.mainHeader + self.icons[iconId][:-2] +
                    b"\x16\x00\x00\x00")
        return None
