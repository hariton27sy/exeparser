import argparse


class Parser:
    def __init__(self, parent):
        usage = ('index.py [-h] filename [-fh] [-oh] [-sh [SH [SH ...]]] '
                 '[-rsh RSH] [-headers]\n\t\t[-exports] '
                 '[-imports] [-dependents] '
                 '[-resources] [-raw]\n\t\t[-relocs] [-sum]')
        description = ('This script allow you to check executable windows '
                       'files.\nYou do not to install requirements if you '
                       'use only CLI version')

        self.parser = argparse.ArgumentParser(description=description,
                                              usage=usage)
        self.parser.add_argument('filename')

        self.parser.add_argument('-fh',
                                 action='store_const',
                                 const=parent.file_header,
                                 help='Prints file header of the file')

        self.parser.add_argument('-oh',
                                 action='store_const',
                                 const=parent.optional_header,
                                 help='Prints optional header of the file')

        self.parser.add_argument('-sh',
                                 action='store',
                                 nargs='*',
                                 default=[-1, -1],
                                 type=int,
                                 help='Takes from 0 to 2 parameters and'
                                      'if 0 parameters print all section info '
                                      'if 1 parameter print section info with '
                                      'number, if 2 params print from 1 number'
                                      ' to 2')

        self.parser.add_argument('-rsh', action='store',
                                 type=int,
                                 help='print raw section that has position of '
                                      'this number in the file')

        self.parser.add_argument('-headers',
                                 action='store_const',
                                 const=parent.headers,
                                 help='Prints file, optional and section'
                                      'headers')

        self.parser.add_argument('-exports',
                                 action='store_const',
                                 const=parent.format_export_table,
                                 help='Print info about export section of the'
                                      'file')

        self.parser.add_argument('-imports',
                                 action='store_const',
                                 const=parent.format_import_table,
                                 help='Print info about imports of the file')

        self.parser.add_argument('-dependents',
                                 action='store_const',
                                 const=parent.format_dependencies,
                                 help='Print info about dependencies')

        self.parser.add_argument('-resources',
                                 action='store_const',
                                 const=parent.get_format_resources,
                                 help='Print resources of the a file')

        self.parser.add_argument('-raw',
                                 action='store_const',
                                 const=parent.get_raw_file,
                                 help='Print hex dump of the file')

        self.parser.add_argument('-relocs',
                                 action='store_const',
                                 const=parent.get_format_relocations,
                                 help='Print relocations of the file')

        self.parser.add_argument('-sum',
                                 action='store_const',
                                 const=parent.get_summary,
                                 help='Print Summary')

    def parse(self, argv):
        return self.parser.parse_args(argv)
