import os

import CLI.file_header as fh
import CLI.optional_header as oh
from CLI.parser import get_parser
from CLI.section_headers import SectionHeaders

from common_funcs import hex_from_bytes, formatted_output, hex_from_number
from core.exefile import ExeFile
from langs import langs


class CommandLineInterface:
    def __init__(self, argv):
        self.curr_lang = 'English'
        self.lang = langs[self.curr_lang]
        self.parser = get_parser(self)

        # Возможно невнимательно
        # просмотрел документацию но
        # по-другому много переписывать
        args = self.parser.parse_args(argv).__dict__

        args['filename'] = os.path.abspath(args['filename'])

        self.exeFile = ExeFile(args['filename'])

        if self.exeFile.exc:
            print(self.exeFile.excInfo)
            return

        self.parse_args(args)

    def parse_args(self, argv):
        print('Dump of file:\n\t' + self.exeFile.path)
        result = []
        for arg in argv:
            if arg == 'section_headers':
                sh = self.section_headers(argv[arg])
                if sh is not None and sh != '':
                    result.append(sh)
            elif arg == 'raw_section_header' and argv[arg]:
                rsh = self.raw_section_data(argv[arg])
                if rsh is not None and rsh != '':
                    result.append(rsh)
            elif arg == 'raw' and argv['raw']:
                argv[arg]()
            elif arg != 'filename' and argv[arg]:
                line = argv[arg]()
                if line is not None and line != '':
                    result.append(line)

        result.append(self.get_summary())

        print('\n'.join(result))

    def file_header(self):
        return str(fh.FileHeader(self.exeFile, self.lang))

    def optional_header(self):
        return str(oh.OptionalHeader(self.exeFile, self.lang))

    def section_headers(self, args):
        return str(SectionHeaders(self.exeFile, self.lang, args))

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
        return (self.file_header() + '\n' +
                self.optional_header() + '\n' +
                self.section_headers([]))

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
            return self.exeFile.resources().get_cli_string('  ')
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
            GUI.resources.ResourcesWidget(self.exeFile)
        except ImportError as e:
            print("I can't run graphic interface. Requirements are missing")


if __name__ == "__main__":
    f = ['-fh', 'examples/firefox2.exe', '-sh', '3']
    CommandLineInterface(f)
