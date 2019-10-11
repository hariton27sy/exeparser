import core.exefile as exe
from common_funcs import hex_from_bytes


def get_line(f, address):
    """find and return line that starts with address and ends by zero-byte
    Parameters:
        f - file stream,
        address - raw address of string"""
    temp_address = f.tell()
    f.seek(address, 0)
    result = f.read(1)
    while result[-1] != 0:
        result += f.read(1)
    f.seek(temp_address, 0)
    return result.decode('utf-8')


def parse_export_table(parent, is_raw=False):
    """Parse export table if it exists. Parameters:

    parent - exeFile object that executes this function"""
    if not isinstance(parent, exe.ExeFile):
        raise TypeError("parent object may be only ExeFile class")
    address, size = map(lambda x: int.from_bytes(x, 'little'),
                        parent.optional_header['dataDirectory'][0])
    if address == 0:
        return None
    address = parent.rva_to_raw(address)[1]
    with open(parent.path, 'rb') as f:
        f.seek(address)
        if is_raw:
            return f.read(size)

        data = f.read(40)
        export_table = {
            'characteristics': hex_from_bytes(data[:4]),
            'timeDataStamp': hex_from_bytes(data[4:8]),
            'version': (str(int.from_bytes(data[8:10], 'little')) + '.' +
                        str(int.from_bytes(data[10:12], 'little'))),
            'name': parent.rva_to_raw(data[12:16])[1],
            'base': int.from_bytes(data[16:20], 'little'),
            'numberOfFunctions': int.from_bytes(data[20:24], 'little'),
            'numberOfNames': int.from_bytes(data[24:28], 'little'),
            'addressesOfFunctions': parent.rva_to_raw(data[28:32])[1],
            'addressesOfNames': parent.rva_to_raw(data[32:36])[1],
            'addressesOfNameOrdinals': parent.rva_to_raw(data[36:40])[1]
        }
        export_table['name'] = get_line(f, export_table['name'])

        return export_table


def parse_import_table(parent):
    """Parses import table. Parameters:

        parent - exeFile object that executes this function"""
    pass
