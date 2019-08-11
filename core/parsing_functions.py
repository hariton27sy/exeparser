import datetime


def parse_file_header(data):
    return {
        'machine': (data[:2], getMachine(data[:2])),
        'numberOfSections': (data[2:4], str(int.from_bytes(data[2:4], 'little'))),
        'creatingTime': (data[4:8], dateFromBytes(data[4:8]).strftime, '%d.%m.%Y %H:%M:%S'),
        'pointerToSymbolTable': (data[8:12], str(int.from_bytes(data[8:12], 'little'))),
        'numberOfSymbols': (data[12:16], str(int.from_bytes(data[12:16], 'little'))),
        'sizeOfOptionalHeader': (data[16:18], str(int.from_bytes(data[16:18], 'little'))),
        'characteristics': (data[18:20], parse_characteristics(data[18:20]))
    }


def parse_optional_header(data):
    # Parsing of all variables without data_directory
    size_of_special_positions = 8 if data[:2] == b'\x0b\x02' else 4
    special = ['linkerVersion', 'operatingSystemVersion', 'imageVersion', 'subsystemVersion']
    optional_header = {'magic': 2, 'linkerVersion': 2, 'sizeOfCode': 4, 'sizeOfInitializedData': 4,
                       'sizeOfUninitializedCode': 4, 'addressOfEntryPoint': 4, 'baseOfCode': 4, 'baseOfData': 4,
                       'imageBase': size_of_special_positions, 'sectionAlignment': 4, 'fileAlignment': 4,
                       'operatingSystemVersion': 4, 'imageVersion': 4, 'subsystemVersion': 4,
                       'win32VersionValue': 4, 'sizeOfImage': 4, 'sizeOfHeaders': 4, 'checkSum': 4, 'subsystem': 2,
                       'dllCharacteristics': 2, 'sizeOfStackReserve': size_of_special_positions,
                       'sizeOfStackCommit': size_of_special_positions, 'sizeOfHeapReserve': size_of_special_positions,
                       'sizeOfHeapCommit': size_of_special_positions, 'loaderFlags': 4, 'numberOfRvaAndSizes': 4}
    pos = 0
    for name in optional_header:
        pos += optional_header[name]
        optional_header[name] = data[pos - optional_header[name]:pos]
        if name in special:
            val = optional_header[name]
            val = '{}.{}'.format(int.from_bytes(val[:len(val) // 2], 'little'),
                                 int.from_bytes(val[len(val) // 2:], 'little'))
            optional_header[name] = (optional_header[name], val)
        elif name == 'magic':
            optional_header[name] = (optional_header[name], getArchitecture(optional_header[name]))
        elif name == 'win32VersionValue':
            optional_header[name] = (optional_header[name], 'Reserved')
        elif name == 'dllCharacteristics':
            optional_header[name] = (optional_header[name], parse_characteristics(optional_header[name]))
        elif name == 'loaderFlags':
            optional_header[name] = (optional_header[name], 'Obsolete')
        else:
            optional_header[name] = (optional_header[name], str(int.from_bytes(optional_header[name], 'little')))

    # Parsing data directory
    data_directory = [(data[i * 8 + pos: i * 8 + pos + 4],
                       data[i * 8 + pos + 4: i * 8 + pos + 8]
                       ) for i in range(int(optional_header['numberOfRvaAndSizes'][1]))]
    optional_header['dataDirectory'] = data_directory
    return optional_header


def dateFromBytes(bytestring):
    binstring = ''
    for b in bytestring:
        binstring = bin(b)[2:].zfill(8) + binstring
    num = int(binstring, 2)
    date = datetime.datetime.utcfromtimestamp(num)
    return date


def getMachine(bytestring):
    matches = {
        b'\x4c\x01': 'x86',
        b'\x00\x02': 'Intel Itanium',
        b'\x64\x86': 'x64'
    }
    if bytestring in matches:
        return matches[bytestring]

    return 'Unknown'


def getArchitecture(bytestring):
    return 'PE64' if bytestring == b'\x0b\x02' else 'PE32'


def parse_characteristics(data):
    binstr = bin(int.from_bytes(data, 'little')).zfill(16)
    return [binstr[-i - 1] == '1' for i in range(16)]

