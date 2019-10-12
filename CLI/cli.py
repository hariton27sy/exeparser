from core.exefile import ExeFile
from langs import langs
from common_funcs import hex_from_bytes, bytes_line_to_symbols, \
    formatted_output


class CommandLineInterface:
    def __init__(self, argv):
        self.keys = {
            '-r': lambda: print('Заглушка'),
            '-fh': lambda: print(self.file_header()),
            '-oh': lambda: print(self.optional_header()),
            '-sh': lambda x, y: print(self.section_headers(range(x, y))),
            '-rsh': lambda x: print(self.raw_section_data(x)),  # TODO:
                                                                #  Limit input
                                                                #  number down
            '-headers': lambda: print('Заглушка'),
            '-a': lambda: print('Заглушка'),
            '--all': lambda: print('Заглушка'),
            '-export': lambda: print(self.format_export_table()),
            '-import': lambda: print(self.format_import_table())
        }

        self.curr_lang = 'English'
        self.lang = langs[self.curr_lang]

        if len(argv) == 0 or argv[0] == '-h' or argv[0] == '--help':
            self.print_help()
            return

        try:
            self.exeFile = ExeFile(argv[-1])
        except Exception as e:
            print(str(e))
            return
        if self.exeFile.exc:
            print(self.exeFile.excInfo)
            return

        self.parse_args(argv)

    def print_help(self):
        print(self.lang.cli_help)

    def parse_args(self, argv):
        for arg in argv:
            pars = arg.split(':')
            if pars[0] == '-sh':
                if len(pars) == 1:
                    self.keys['-sh'](0, int(self.exeFile.file_header
                                            ['numberOfSections'][1]))
                elif len(pars) == 2:
                    self.keys['-sh'](int(pars[1]) - 1, int(pars[1]))
                else:
                    self.keys['-sh'](int(pars[1]) - 1, int(pars[2]))
            elif pars[0] == '-rsh' and len(pars) == 2:
                self.keys['-rsh'](int(pars[1]))
            elif pars[0] in self.keys:
                self.keys[pars[0]]()

    def file_header(self):
        file_header_lang = self.lang.headers_info[1]['file_header']
        result = f'{file_header_lang[0].upper()}:\n'
        for key in self.exeFile.file_header:
            val = self.exeFile.file_header[key]
            interpreted_value = val[1]
            if key == 'creatingTime':
                date_form = file_header_lang[2]['creatingTime'][
                    1] if isinstance(
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
            field_name = (file_header_lang[2][key][0] if isinstance(
                file_header_lang[2][key], tuple) else
                          file_header_lang[2][key])
            result += '{0:>16} | {1:<30} {2}\n'.format(hex_from_bytes(val[0]),
                                                       field_name,
                                                       interpreted_value)

        return result

    def optional_header(self):
        def data_directories(interface):
            result = ''
            localisation = interface.lang.data_directory_tab[2]
            data_directory = interface.exeFile.optional_header['dataDirectory']
            for i in range(int(
                    interface.exeFile.optional_header['numberOfRvaAndSizes'][
                        1])):
                if localisation[i] is not None:
                    result += '{0:>16} [{1:>10}] RVA [size] of {2}\n'.format(
                        hex_from_bytes(data_directory[i][0]),
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
                interpreted_value = '| ' + (
                    optional_header_lang[key][1][int(interpreted_value)]
                    if int(interpreted_value) in
                       optional_header_lang[key][1] else
                    optional_header_lang[key][2]) + '\n'
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
            result += '{0:>16} | {1:<30} {2}'.format(hex_from_bytes(val[0]),
                                                     field_name,
                                                     interpreted_value)

        result += data_directories(self)

        return result

    def section_headers(self, args):
        localisation = self.lang.section_headers_tab[1]
        sections = self.exeFile.section_headers
        result = []
        for section_number in args:
            if section_number > int(self.exeFile.file_header
                                    ['numberOfSections'][1]):
                continue
            temp = ''
            if section_number >= len(sections):
                break
            temp += f'SECTION HEADER #{section_number + 1}\n'
            line_index = 0
            for line in sections[section_number]:
                field = hex_from_bytes(
                    sections[section_number][line]) if line != 'name' else \
                    sections[section_number][line]
                temp += f'{field:>12} {localisation[line_index]}\n'
                line_index += 1
            result.append(temp)

        return '\n'.join(
            result)  # TODO: make to return list of sections in right format

    def raw_section_data(self, section_number):
        if section_number > int(self.exeFile.file_header
                                ['numberOfSections'][1]):
            return ''
        section = self.exeFile.section_headers[section_number - 1]
        base_address = int.from_bytes(section['virtualAddress'], 'little')
        title = f'RAW SECTION #{section_number}\n'
        return title + formatted_output(base_address,
                                        self.exeFile.raw_section_data(
                                            section_number))

        result = f'{self.section_headers([section_number])}\n\n'
        line = f'{hex(base_address):>10}:'
        counter = 0
        for ch in self.exeFile.raw_section_data(section_number):
            if counter != 0 and counter % 16 == 0:
                result += line + ' ' + bytes_line_to_symbols(line[11:])
                line = f'\n{hex(base_address + counter):>10}:'
            line += f' {hex(ord(ch))[2:].upper():0^2s}'
            counter += 1

        return result

    def headers(self):
        return (self.file_header() +
                self.optional_header() +
                self.section_headers(range(1, int(self.exeFile.file_header
                                                  ['numberOfSections'][
                                                      1]) + 1)))

    def format_import_table(self):
        import_table = self.exeFile.import_table()
        result = 'Section contains the following imports:\n\n'
        for element in import_table:
            result += f'\t{element["name"]}\n\t' \
                      f'{hex(element["originalFirstThunk"]):>12} ' \
                      'Import Address Table\n\t' \
                      f'{hex(element["firstThunk"]):>12} ' \
                      'Import Name Table\n\t' \
                      f'{hex(element["timeDateStamp"]):>12} ' \
                      'TimeDate Stamp\n\t' \
                      f'{hex(element["forwarderChain"]):>12} ' \
                      'Index of first forwarder reference\n\n'
        return result

    def format_export_table(self):
        export_table = self.exeFile.export_table()
        if export_table is None:
            return ''
        result = ('    Section contains the following exports for '
                  f'{export_table["name"]}\n\t'
                  f'{export_table["characteristics"]:>12} Characteristics\n\t'
                  f'{export_table["timeDateStamp"]:>12} TimeDate Stamp\n\t'
                  f'{export_table["version"]:>12} Version\n\t'
                  f'{export_table["base"]:>12} Base\n\t'
                  f'{export_table["numberOfFunctions"]:>12} '
                  'Number of Functions\n\t'
                  f'{export_table["numberOfNames"]:>12} Number of Names\n\n\t')

        result += f'ordinal hint {"RVA":>10} name\n\n\t'
        for i in range(export_table['numberOfNames']):
            rva = (export_table["addressesOfFunctions"]
                                [export_table["nameOrdinals"][i] - 1])
            result += (f'{export_table["nameOrdinals"][i]:>7} {hex(i)[2:]:>4} '
                       f'{rva:>10} {export_table["names"][i]}\n\t')
        return result
