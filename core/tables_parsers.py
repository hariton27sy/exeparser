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
    try:
        return result[:-1].decode('utf-8')
    except Exception as e:
        return ""


def parse_data_to_array(data, cell_size: int, func):
    """Parses data(bytes object) to array using function 'func'
    Every cell has size cell_size in 'data'.

    Parameters:
        data - bytes/byteArray object. len(data)
        Must be a multiple of cell_size
        cell_size - int object
        func - func that transforms input_data"""
    result = []
    if len(data) % cell_size != 0:
        raise ValueError("Length of data must be a multiple of cell_size")
    for i in range(len(data) // cell_size):
        result.append(func(data[i * cell_size:(i + 1) * cell_size]))

    return result


def parse_export_table(parent, is_raw=False):
    """Parse export table if it exists. Parameters:

    parent - exeFile object that executes this function"""
    # if not isinstance(parent, ExeFile):
    #     raise TypeError("parent object may be only ExeFile class")
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

        # Parsing names of functions
        f.seek(export_table['addressesOfNames'], 0)
        array_data = f.read(export_table['numberOfNames'] * 4)
        parse_method = lambda x: get_line(f, parent.rva_to_raw(x)[1])
        export_table['addressesOfNames'] = parse_data_to_array(array_data, 4,
                                                               parse_method)

        # Parsing ordinals
        f.seek(export_table['addressesOfNameOrdinals'])
        array_data = f.read(export_table['numberOfNames'] * 2)
        parse_method = lambda x: int.from_bytes(x, 'little') + 1
        export_table['addressesOfNameOrdinals'] = parse_data_to_array(
            array_data, 2,
            parse_method)

        # Parsing names of functions
        # TODO: Difference RVA (see documentation)
        f.seek(export_table['addressesOfFunctions'])
        array_data = f.read(export_table['numberOfFunctions'] * 4)
        parse_method = lambda x: hex_from_bytes(x)
        export_table['addressesOfFunctions'] = parse_data_to_array(
            array_data, 4,
            parse_method)

        return export_table


def parse_import_table(parent):
    """Parses import table. Parameters:

        parent - exeFile object that executes this function"""
    address, size = map(lambda x: int.from_bytes(x, 'little'),
                        parent.optional_header['dataDirectory'][1])

    if address == 0:
        return None
    result = []
    with open(parent.path, 'rb') as f:
        f.seek(parent.rva_to_raw(address)[1])
        zero_struct = bytes(0 for _ in range(20))
        data = f.read(20)
        while data != zero_struct:
            result.append({
                'originalFirstThunk': parent.rva_to_raw(data[:4])[1],
                'timeDateStamp': int.from_bytes(data[4:8], 'little'),
                'forwarderChain': int.from_bytes(data[8:12], 'little'),
                'name': get_line(f, parent.rva_to_raw(data[12:16])[1]),
                'firstThunk': parent.rva_to_raw(data[16:20])[1]
            })
            data = f.read(20)

        return result
