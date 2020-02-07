from common_funcs import hex_from_bytes


def data_directories(interface):
    result = []
    localisation = interface.lang.data_directory_tab[2]
    data_directory = interface.exeFile.optional_header['dataDirectory']
    for i in range(int(
            interface.exeFile.optional_header['numberOfRvaAndSizes'][1])):
        if localisation[i] is not None:
            result.append('{num:0>2}){0:>16} [{1:>10}] RVA [size] of {2}\n'.
                          format(hex_from_bytes(data_directory[i][0]),
                                 hex_from_bytes(data_directory[i][1]),
                                 localisation[i], num=i + 1))

    return "".join(result)


class OptionalHeader:
    def __init__(self, exeFile, lang):
        self.exeFile = exeFile
        self.lang = lang

    def __str__(self):
        optional_header_lang = self.lang.headers_info[1]['optional_header']
        result = [f'{optional_header_lang[0].upper()}:\n']
        optional_header_lang = optional_header_lang[2]
        # print(self.exeFile.optional_header)
        for key in self.exeFile.optional_header:
            if key == 'dataDirectory' or optional_header_lang[key] is None:
                continue
            val = self.exeFile.optional_header[key]
            interpreted_value = val[1]
            if key == 'subsystem':
                interpreted_value = '| ' + (
                    optional_header_lang[key][1][int(interpreted_value)]
                    if int(interpreted_value) in optional_header_lang[key][1]
                    else optional_header_lang[key][2])
                field_name = optional_header_lang[key][0]
            elif key == 'dllCharacteristics':
                flags = interpreted_value
                interpreted_value = ['']
                names = optional_header_lang['dllCharacteristics'][1]
                for _id in range(len(flags)):
                    if flags[_id] and names[_id] is not None:
                        interpreted_value.append('\t\t\t{}'.format(names[_id]))
                interpreted_value = "\n".join(interpreted_value)
                field_name = optional_header_lang[key][0]
            else:
                interpreted_value = f'| {interpreted_value}'
                field_name = optional_header_lang[key]
            result.append(
                '{0:>16} | {1:<30} {2}'.format(hex_from_bytes(val[0]),
                                               field_name, interpreted_value))

        result.append(data_directories(self))

        return "\n".join(result)
