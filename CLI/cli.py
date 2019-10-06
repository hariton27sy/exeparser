from core.exefile import ExeFile
from langs import langs
from common_funcs import hex_from_bytes, bytes_line_to_symbols


class CommandLineInterface:
    def __init__(self, argv):
        self.keys = {
            '-r': (0, lambda: print('-r')),
            '-f': (1, lambda: print('-f')),
            '-fh': (0, lambda: print(self.file_header())),
            '-oh': (0, lambda: print(self.optional_header())),
            '-sh': (0, lambda: print(self.section_headers(range(6))))
        }

        self.curr_lang = 'English'
        self.lang = langs[self.curr_lang]

        self.exeFile = ExeFile('examples/qoob.exe')
        if len(argv) == 0 or argv[0] == '-h' or argv[0] == '--help':
            self.print_help()
            return

        self.parse_args(argv)

    def print_help(self):
        print(self.lang.cli_help)

    def parse_args(self, argv):
        print(argv[0])
        if len(argv) > 0 and argv[0] in self.keys:
            self.keys[argv[0]][1]()
        # self.file_header()
        # self.optional_header()
        # self.section_headers(range(6))

    def file_header(self):
        file_header_lang = self.lang.headers_info[1]['file_header']
        result = f'{file_header_lang[0].upper()}:\n'
        for key in self.exeFile.file_header:
            val = self.exeFile.file_header[key]
            interpreted_value = val[1]
            if key == 'creatingTime':
                date_form = file_header_lang[2]['creatingTime'][1] if isinstance(
                    file_header_lang[2]['creatingTime'], tuple) else val[2]
                interpreted_value = interpreted_value(date_form)
            if key == 'characteristics':
                flags = interpreted_value
                interpreted_value = ''
                names = file_header_lang[2]['characteristics'][1]
                for id in range(len(flags)):
                    if flags[id] and names[id] is not None:
                        interpreted_value += '\n\t\t\t{}'.format(names[id])
            else:
                interpreted_value = '| ' + interpreted_value
            field_name = (file_header_lang[2][key][0] if isinstance(file_header_lang[2][key], tuple) else
                          file_header_lang[2][key])
            result += '{0:>16} | {1:<30} {2}\n'.format(hex_from_bytes(val[0]), field_name, interpreted_value)

        return result

    def optional_header(self):
        def data_directories(interface):
            result = ''
            localisation = interface.lang.data_directory_tab[2]
            data_directory = interface.exeFile.optional_header['dataDirectory']
            for i in range(int(interface.exeFile.optional_header['numberOfRvaAndSizes'][1])):
                if localisation[i] is not None:
                    result += '{0:>16} [{1:>10}] RVA [size] of {2}\n'.format(hex_from_bytes(data_directory[i][0]),
                                                                             hex_from_bytes(data_directory[i][1]),
                                                                             localisation[i])

            return result

        optional_header_lang = self.lang.headers_info[1]['optional_header']
        result = f'{optional_header_lang[0].upper()}:\n'
        optional_header_lang = optional_header_lang[2]
        # print(self.exeFile.optional_header)
        for key in self.exeFile.optional_header:
            if key == 'dataDirectory' or optional_header_lang[key] is None:
                continue
            val = self.exeFile.optional_header[key]
            interpreted_value = val[1]
            if key == 'subsystem':
                interpreted_value = '| ' + (optional_header_lang[key][1][int(interpreted_value)]
                                            if int(interpreted_value) in
                                               optional_header_lang[key][1] else optional_header_lang[key][2]) + '\n'
                field_name = optional_header_lang[key][0]
            elif key == 'dllCharacteristics':
                flags = interpreted_value
                interpreted_value = '\n'
                names = optional_header_lang['dllCharacteristics'][1]
                for _id in range(len(flags)):
                    if flags[_id] and names[_id] is not None:
                        interpreted_value += '\t\t\t{}\n'.format(names[_id])
                field_name = optional_header_lang[key][0]
            else:
                interpreted_value = f'| {interpreted_value}\n'
                field_name = optional_header_lang[key]
            result += '{0:>16} | {1:<30} {2}'.format(hex_from_bytes(val[0]), field_name, interpreted_value)

        result += data_directories(self)

        return result

    def section_headers(self, args):
        localisation = self.lang.section_headers_tab[1]
        sections = self.exeFile.section_headers
        result = []
        for section_number in args:
            temp = ''
            if section_number >= len(sections):
                break
            section_name = list(sections.keys())[section_number]
            temp += f'SECTION HEADER #{section_number + 1}\n{section_name:>12} {localisation[0]}\n'
            line_index = 1
            for line in sections[section_name]:
                temp += f'{hex_from_bytes(sections[section_name][line]):>12} {localisation[line_index]}\n'
                line_index += 1
            result.append(temp)

        return '\n'.join(result)  # TODO: make to return list of sections in right format

    def raw_section_data(self, section_number):
        section = self.exeFile.section_headers[section_number - 1]
        base_address = int.from_bytes(section['virtualAddress'], 'little')
        result = f'RAW SECTION #{section_number}\n'
        line = ''
        counter = 0
        for ch in self.exeFile.raw_section_data(section_number):
            if counter != 0 and counter % 16 == 0:
                line = f'\n{hex(base_address + counter):>10}:'
            line += f' {hex(ch).upper()}'
