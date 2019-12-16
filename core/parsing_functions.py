import datetime
import struct


def parse_file_header(data):
    """return dictionary of File Header in format
        tuple(raw_data, description of data[, standard print format]) or
        tuple(raw_data, list )"""
    unpacked = struct.unpack("HHIIIHH", data)
    return {
        'machine': (data[:2], getMachine(data[:2])),
        'numberOfSections': (data[2:4], str(unpacked[1])),
        'creatingTime': (data[4:8], datetime.datetime
                         .fromtimestamp(unpacked[2]).strftime,
                         '%d.%m.%Y %H:%M:%S'),
        'pointerToSymbolTable': (data[8:12], str(unpacked[3])),
        'numberOfSymbols': (data[12:16], str(unpacked[4])),
        'sizeOfOptionalHeader': (data[16:18], str(unpacked[5])),
        'characteristics': (data[18:20], parse_characteristics(data[18:20]))
    }


def parse_optional_header(data):
    """Return Optional Header dictionary in format
        tuple(raw_data, description of data[, standard print format]) or
        tuple(raw_data, list )"""
    # Parsing of all variables without data_directory
    size_of_special_positions = 8 if data[:2] == b'\x0b\x02' else 4
    special_size_2 = 0 if data[:2] == b'\x0b\x02' else 4
    special = ['linkerVersion', 'operatingSystemVersion', 'imageVersion',
               'subsystemVersion']
    optional_header = {'magic': 2, 'linkerVersion': 2, 'sizeOfCode': 4,
                       'sizeOfInitializedData': 4,
                       'sizeOfUninitializedCode': 4,
                       'addressOfEntryPoint': 4, 'baseOfCode': 4,
                       'baseOfData': special_size_2,
                       'imageBase': size_of_special_positions,
                       'sectionAlignment': 4, 'fileAlignment': 4,
                       'operatingSystemVersion': 4, 'imageVersion': 4,
                       'subsystemVersion': 4,
                       'win32VersionValue': 4, 'sizeOfImage': 4,
                       'sizeOfHeaders': 4, 'checkSum': 4, 'subsystem': 2,
                       'dllCharacteristics': 2,
                       'sizeOfStackReserve': size_of_special_positions,
                       'sizeOfStackCommit': size_of_special_positions,
                       'sizeOfHeapReserve': size_of_special_positions,
                       'sizeOfHeapCommit': size_of_special_positions,
                       'loaderFlags': 4, 'numberOfRvaAndSizes': 4}
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
            optional_header[name] = (optional_header[name],
                                     getArchitecture(optional_header[name]))
        elif name == 'win32VersionValue':
            optional_header[name] = (optional_header[name], 'Reserved')
        elif name == 'dllCharacteristics':
            optional_header[name] = (optional_header[name],
                                     parse_characteristics(
                                         optional_header[name]))
        elif name == 'loaderFlags':
            optional_header[name] = (optional_header[name], 'Obsolete')
        else:
            optional_header[name] = (optional_header[name], str(int.from_bytes(
                optional_header[name], 'little')))

    # Parsing data directory
    data_directory = [(data[i * 8 + pos: i * 8 + pos + 4],
                       data[i * 8 + pos + 4: i * 8 + pos + 8]
                       ) for i in range(int(
                        optional_header['numberOfRvaAndSizes'][1]))]
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
    """Return Type of a Machine from bytestring in string format"""
    matches = {
        b'\x4c\x01': 'x86',
        b'\x00\x02': 'Intel Itanium',
        b'\x64\x86': 'x64'
    }
    if bytestring in matches:
        return matches[bytestring]

    return 'Unknown'


def parse_section_headers(data):
    sections = []
    for i in range(len(data) // 40):
        pos = i * 40
        name = data[pos:pos + 8].strip(b'\x00').decode('utf-8')
        sections.append({
            'name': name,
            'virtualSize': data[pos + 8:pos + 12],
            'virtualAddress': data[pos + 12:pos + 16],
            'sizeOfRawData': data[pos + 16:pos + 20],
            'pointerToRawData': data[pos + 20:pos + 24],
            'pointerToRelocations': data[pos + 24:pos + 28],
            'pointerToLineNumbers': data[pos + 28:pos + 32],
            'numberOfRelocations': data[pos + 32:pos + 34],
            'numberOfNumberLines': data[pos + 34:pos + 36],
            'characteristics': data[pos + 36:pos + 40]
        })

    return sections


def getArchitecture(bytestring):
    return 'PE64' if bytestring == b'\x0b\x02' else 'PE32'


def parse_characteristics(data):
    binstr = bin(int.from_bytes(data, 'little')).zfill(16)
    return [binstr[-i - 1] == '1' for i in range(16)]
