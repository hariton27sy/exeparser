import datetime


def parse_file_header(data):
    return {'machine': getArchitecture(data[:2]),
            'numberOfSections': int.from_bytes(data[2:4], 'little'),
            'creatingTime': dateFromBytes(data[4:8]),
            'pointerToSymbolTable': int.from_bytes(data[8:12], 'little'),
            'numberOfSymbols': int.from_bytes(data[12:16], 'little'),
            'sizeOfOptionalHeader': int.from_bytes(data[16:18], 'little'),
            'characteristics': data[18:20]}


def parse_optional_header(data):
    # TODO: Make parsing of x64 files
    size_of_special_positions = 8 if data[:2] == b'\x0b\x02' else 4
    optional_header = {
        'magic': data[:2],
        'linkerVersion': (data[2], data[3]),
        'sizeOfCode': data[4:8],
        'sizeOfInitializedData': data[8:12],
        'sizeOfUninitializedCode': data[12:16],
        'addressOfEntryPoint': data[16:20],
        'baseOfCode': data[20:24],
        'baseOfData': data[24:28],
        'imageBase': data[28:28 + size_of_special_positions],
        'sectionAlignment': data[32:36],
        'fileAlignment': data[36:40],
        'majorOperatingSystemVersion': data[40:42],
        'minorOperatingSystemVersion': data[42:44],
        'majorImageVersion': data[44:46],
        'minorImageVersion': data[46:48],
        'majorSubsystemVersion': data[48:50],
        'minorSubsystemVersion': data[50:52],
        'win32VersionValue': data[52:56],
        'sizeOfImage': data[56:60],
        'sizeOfHeaders': data[60:64],
        'checkSum': data[64:68],
        'subsystem': data[68:70],
        'dllCharacteristics': data[70:72],
        'sizeOfStackReserve': data[72:76],
        'sizeOfStackCommit': data[76:80],
        'sizeOfHeapReserve': data[80:84],
        'sizeOfHeapCommit': data[84:88],
        'loaderFlags': data[88:92],
        'numberOfRvaAndSizes': int.from_bytes(data[92:96], 'little')
    }

    data_directory = [(int.from_bytes(data[i * 8 + 96: i * 8 + 100], 'little'),
                       int.from_bytes(data[i * 8 + 100: i * 8 + 104], 'little')
                       ) for i in range(optional_header['numberOfRvaAndSizes'])]
    optional_header['dataDirectory'] = data_directory
    return optional_header


def dateFromBytes(bytestring):
    binstring = ''
    for b in bytestring:
        binstring = bin(b)[2:].zfill(8) + binstring
    num = int(binstring, 2)
    date = datetime.datetime.utcfromtimestamp(num)
    return date


def getArchitecture(bytestring):
    matches = {
        b'\x4c\x01': 'x86',
        b'\x00\x02': 'Intel Itanium',
        b'\x64\x86': 'x64'
    }
    if bytestring in matches:
        return bytestring, matches[bytestring]

    return bytestring, 'Unknown'
