from common_funcs import get_line, hex_from_bytes


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


class ExportTable:
    def __init__(self, parent):
        self.parent = parent
        self.table = self.parse_export_table()

    def parse_export_table(self):
        """Parse export table if it exists. Parameters:

        parent - exeFile object that executes this function"""
        # if not isinstance(parent, ExeFile):
        #     raise TypeError("parent object may be only ExeFile class")
        address, size = map(lambda x: int.from_bytes(x, 'little'),
                            self.parent.optional_header['dataDirectory'][0])
        if address == 0:
            return None
        address = self.parent.rva_to_raw(address)[1]
        with open(self.parent.path, 'rb') as f:
            f.seek(address)

            data = f.read(40)
            export_table = {
                'characteristics': hex_from_bytes(data[:4]),
                'timeDateStamp': hex_from_bytes(data[4:8]),
                'version': (str(int.from_bytes(data[8:10], 'little')) + '.' +
                            str(int.from_bytes(data[10:12], 'little'))),
                'name': self.parent.rva_to_raw(data[12:16])[1],
                'base': int.from_bytes(data[16:20], 'little'),
                'numberOfFunctions': int.from_bytes(data[20:24], 'little'),
                'numberOfNames': int.from_bytes(data[24:28], 'little'),
                'addressesOfFunctions': self.parent.rva_to_raw(data[28:32])[1],
                'addressesOfNames': self.parent.rva_to_raw(data[32:36])[1],
                'addressesOfNameOrdinals': self.parent.rva_to_raw(data
                                                                  [36:40])[1]
            }
            export_table['name'] = get_line(f, export_table['name'])

            # Parsing names of functions
            f.seek(export_table['addressesOfNames'], 0)
            array_data = f.read(export_table['numberOfNames'] * 4)
            export_table['names'] = parse_data_to_array(
                array_data, 4,
                lambda x: get_line(f, self.parent.rva_to_raw(x)[1]))

            # Parsing ordinals
            f.seek(export_table['addressesOfNameOrdinals'])
            array_data = f.read(export_table['numberOfNames'] * 2)
            export_table['nameOrdinals'] = parse_data_to_array(
                array_data, 2,
                lambda x: int.from_bytes(x, 'little') + 1)

            # Parsing names of functions
            # TODO: Difference RVA (see documentation)
            f.seek(export_table['addressesOfFunctions'])
            array_data = f.read(export_table['numberOfFunctions'] * 4)
            export_table['addressesOfFunctions'] = parse_data_to_array(
                array_data, 4,
                lambda x: hex_from_bytes(x))

            return export_table

    def __str__(self):
        if self.table is None:
            return ''
        result = ['    Section contains the following exports for '
                  f'{self.table["name"]}\n\t'
                  f'{self.table["characteristics"]:>12} Characteristics\n\t'
                  f'{self.table["timeDateStamp"]:>12} TimeDate Stamp\n\t'
                  f'{self.table["version"]:>12} Version\n\t'
                  f'{self.table["base"]:>12} Base\n\t'
                  f'{self.table["numberOfFunctions"]:>12} '
                  'Number of Functions\n\t'
                  f'{self.table["numberOfNames"]:>12} Number of Names\n\n\t',
                  f'ordinal hint {"RVA":>10} name\n\n\t']

        for i in range(self.table['numberOfNames']):
            rva = (self.table["addressesOfFunctions"]
                   [self.table["nameOrdinals"][i] - 1])
            result.append(f'{self.table["nameOrdinals"][i]:>7} '
                          f'{hex(i)[2:]:>4} {rva:>10} '
                          f'{self.table["names"][i]}\n\t')
        return "".join(result)
