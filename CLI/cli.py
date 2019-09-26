from core.exefile import ExeFile
from langs import langs
from common_funcs import hex_from_bytes


class CommandLineInterface:
    def __init__(self, argv):
        self.keys = {
            '-r': (0, "delegate"),
            '-f': (1, "delegate"),
            '-fh': (0, self.file_header),
            '-oh': (0, self.optional_header)
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
        self.file_header()
        self.optional_header()
        self.data_directories()

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

        print(result)
        return result

    def optional_header(self):
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
                interpreted_value = (optional_header_lang[key][1][int(interpreted_value)]
                                     if int(interpreted_value) in
                                     optional_header_lang[key][1] else optional_header_lang[key][2])
                print(interpreted_value)
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
                interpreted_value = '| ' + interpreted_value
                field_name = optional_header_lang[key]
            result += '{0:>16} | {1:<30} {2}\n'.format(hex_from_bytes(val[0]), field_name, interpreted_value)

        print(result)
        return result + self.data_directories()

    def data_directories(self):
        result = ''
        localisation = self.lang.data_directory_tab[2]
        data_directory = self.exeFile.optional_header['dataDirectory']
        for i in range(int(self.exeFile.optional_header['numberOfRvaAndSizes'][1])):
            if localisation[i] is not None:
                result += '{0:>16} [{1:>10}] RVA [size] of {2}\n'.format(hex_from_bytes(data_directory[i][0]),
                                                                       hex_from_bytes(data_directory[i][1]),
                                                                       localisation[i])

        print(result)
        return result
