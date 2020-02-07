from common_funcs import get_line, hex_from_bytes


def string_functions(element):
    return "\n".join(
        map(lambda func: f"\t{hex_from_bytes(func[0], -1)[2:]:>12} {func[1]}",
            element['functions']))


class ImportTable:
    def __init__(self, parent):
        self.parent = parent
        self.table = self._parse_import_table()

    def _parse_import_table(self):
        """Parses import table. Parameters:

            parent - exeFile object that executes this function"""
        address, size = map(lambda x: int.from_bytes(x, 'little'),
                            self.parent.optional_header['dataDirectory'][1])

        if address == 0:
            return None
        result = []
        with open(self.parent.path, 'rb') as f:
            f.seek(self.parent.rva_to_raw(address)[1])
            zero_struct = b"\x00" * 20
            data = f.read(20)
            while data != zero_struct:
                result.append({
                    'originalFirstThunk': int.from_bytes(data[:4], 'little'),
                    'timeDateStamp': int.from_bytes(data[4:8], 'little'),
                    'forwarderChain': int.from_bytes(data[8:12], 'little'),
                    'name':
                        get_line(f, self.parent.rva_to_raw(data[12:16])[1]),
                    'firstThunk': int.from_bytes(data[16:20], 'little')
                })
                result[-1]['functions'] = self._get_functions(
                    f, self.parent.rva_to_raw(
                        result[-1]['firstThunk'])[1])
                result[-1]['type'] = result[-1]['name'].split('.')[-1]
                data = f.read(20)
            result.sort(key=lambda e: e['type'], reverse=True)
            return result

    def __str__(self):
        if self.table is None:
            return ''
        result = ['Section contains the following imports:\n\n']
        for element in sorted(self.table, key=lambda x: x['name']):
            result.append(f'\t{element["name"]}\n\t'
                          f'{hex(element["firstThunk"]):>12} '
                          'Import Address Table\n\t'
                          f'{hex(element["originalFirstThunk"]):>12} '
                          'Import Name Table\n\t'
                          f'{hex(element["timeDateStamp"]):>12} '
                          'TimeDate Stamp\n\t'
                          f'{hex(element["forwarderChain"]):>12} '
                          'Index of first forwarder reference\n\n'
                          f'{string_functions(element)}\n\n')
        return "".join(result)

    def get_dependencies(self):
        result = set()
        for elem in self.table:
            result.add(elem['name'])
        result = list(result)
        return sorted(result, key=lambda e: e.split('.')[-1], reverse=True)

    def _get_functions(self, file, address):
        result = []
        start_address = file.tell()
        file.seek(address)
        size = 4 if self.parent.optional_header['magic'][1] == 'PE32' else 8
        lookup_table = int.from_bytes(file.read(size), 'little')
        while lookup_table != 0:
            if lookup_table < 8 * (16 ** (size * 2 - 1)):
                temp = file.tell()
                raw = self.parent.rva_to_raw(lookup_table)[1]
                file.seek(raw)
                result.append((file.read(2), get_line(file, raw + 2)))
                file.seek(temp)

            lookup_table = int.from_bytes(file.read(size), 'little')

        file.seek(start_address)
        return result
