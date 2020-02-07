import os

import CLI.file_header as fh
import CLI.optional_header as oh
from CLI.parser import get_parser
from CLI.section_headers import SectionHeaders

from common_funcs import formatted_output, hex_from_number
from core.exefile import ExeFile
from langs import en


class CommandLineInterface:
    def __init__(self, argv):
        self.lang = en
        self.parser = get_parser(self)

        args = self.parser.parse_args(argv)

        self.exeFile = ExeFile(os.path.abspath(args.filename))

        if self.exeFile.exc:
            print(self.exeFile.excInfo)
            return

        self.parse_args(args)

    def parse_args(self, argv):
        result = ['Dump of file:\n\t' + self.exeFile.path]
        if argv.funcs:
            result.extend([e() for e in argv.funcs])

        if argv.section_headers is not None:
            result.append(self.section_headers(argv.section_headers))
        if argv.data_directory_raw:
            result.append(self.raw_data_directory(argv.data_directory_raw))
        if argv.raw_section_header:
            result.append(self.raw_section_data(argv.raw_section_header))
        if argv.full_section_header:
            result.append(self.section_headers([argv.full_section_header]))
            result.append(self.raw_section_data(argv.full_section_header))

        print("\n".join(result))

        if argv.raw:
            argv.raw()

    def file_header(self):
        return str(fh.FileHeader(self.exeFile, self.lang))

    def optional_header(self):
        return str(oh.OptionalHeader(self.exeFile, self.lang))

    def section_headers(self, args):
        return "\n" + str(SectionHeaders(self.exeFile, self.lang, args))

    def raw_section_data(self, section_number):
        if section_number > int(self.exeFile.file_header
                                ['numberOfSections'][1]):
            return ''
        section = self.exeFile.section_headers[section_number - 1]
        base_address = int.from_bytes(section['virtualAddress'], 'little')
        title = f'RAW SECTION #{section_number}\n'
        return title + "".join(formatted_output(base_address,
                                                self.exeFile.raw_section_data(
                                                    section_number)))

    def headers(self):
        return "\n".join([self.file_header(), self.optional_header(),
                         self.section_headers([])])

    def format_import_table(self):
        return str(self.exeFile.import_table())

    def format_export_table(self):
        return str(self.exeFile.export_table())

    def format_dependencies(self):
        import_table = self.exeFile.import_table()
        if import_table is None:
            return ''
        dependencies = import_table.get_dependencies()
        return ("  Image has the following dependencies:\n\t" + '\n\t'.
                join(dependencies))

    def get_format_resources(self):
        resources = self.exeFile.resources()
        if resources is not None:
            result = [self.exeFile.resources().get_cli_string('  '),
                      "\n String Resources"]
            result.extend(map(lambda x: f"   {x}",
                              self.exeFile.string_resources()))
            if len(result) == 2:
                del result[-1]
            return '\n'.join(result)
        return ""

    def get_raw_file(self):
        for line in formatted_output(0, self.exeFile.raw_data()):
            print(line, end='')

    def get_format_relocations(self):
        relocs = self.exeFile.relocations()
        if relocs is None:
            return ''
        return relocs.get_str()

    def get_summary(self):
        summary = self.exeFile.get_summary()
        result = ['Summary:', '     SectionName Size']
        for elem in summary:
            result.append(f'\t{elem[0]:>8} {hex_from_number(elem[1])}')

        return '\n'.join(result)

    def graphic_resources(self):
        try:
            import GUI.resources
            GUI.resources.get_resource_widget_as_main(self.exeFile)
        except ImportError as e:
            print("I can't run graphic interface. Requirements are missing")

    def raw_data_directory(self, number):
        number_of_rva = self.exeFile.optional_header['numberOfRvaAndSizes'][1]
        if number < 1 or number > int(number_of_rva):
            return f"Please enter the number from 1 to {number_of_rva}"
        data_directory = (self.exeFile.optional_header[
            'dataDirectory'][number - 1])
        data_directory = (int.from_bytes(data_directory[0], 'little'),
                          int.from_bytes(data_directory[1], 'little'))

        data = self.exeFile.raw_data(data_directory)

        return (f"RAW DATA DIRECTORY #{number} "
                f"({self.lang.data_directory_tab[2][number - 1]})\n" +
                "".join(formatted_output(data_directory[0], data)))
