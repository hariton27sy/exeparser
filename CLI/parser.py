import argparse


def get_parser(parent):
    description = ('This script allow you to check executable windows '
                   'files.\nYou do not to install requirements if you '
                   'use only CLI version')

    parser = argparse.ArgumentParser(description=description)

    # OK
    parser.add_argument('--file-header',
                        action='append_const',
                        dest='funcs',
                        const=parent.file_header,
                        help='Prints file header of the file')

    # OK
    parser.add_argument('--optional-header',
                        action='append_const',
                        dest='funcs',
                        const=parent.optional_header,
                        help='Prints optional header of the file')

    # OK
    parser.add_argument('--data-directory-raw', action='store',
                        type=int,
                        help="Print raw dump of data directory which has "
                             "this position")

    # OK
    parser.add_argument('--section-headers',
                        action='store',
                        nargs='*',
                        type=int,
                        help='Takes from 0 to 2 parameters and'
                             'if 0 parameters print all section info '
                             'if 1 parameter print section info with '
                             'number, if 2 params print from 1 number'
                             ' to 2')

    # OK
    parser.add_argument('--raw-section-header', action='store',
                        type=int,
                        help='print raw dump section that has position of '
                             'this number in the file')

    # OK
    parser.add_argument('--full-section-header', action='store',
                        type=int,
                        help='print full information with dump about section '
                             'that has this number')

    # OK
    parser.add_argument('--headers',
                        action='append_const',
                        dest='funcs',
                        const=parent.headers,
                        help='Prints file, optional and section'
                             'headers')

    # OK
    parser.add_argument('--exports',
                        action='append_const',
                        dest='funcs',
                        const=parent.format_export_table,
                        help='Print info about export section of the'
                             'file')

    # OK
    parser.add_argument('--imports',
                        action='append_const',
                        dest='funcs',
                        const=parent.format_import_table,
                        help='Print info about imports of the file')

    # OK
    parser.add_argument('--dependents',
                        action='append_const',
                        dest='funcs',
                        const=parent.format_dependencies,
                        help='Print info about dependencies')

    # OK
    parser.add_argument('--resources',
                        action='append_const',
                        dest='funcs',
                        const=parent.get_format_resources,
                        help='Print resources of the a file')

    # OK
    parser.add_argument('--raw',
                        action='store_const',
                        const=parent.get_raw_file,
                        help='Print hex dump of the file')

    # OK
    parser.add_argument('--relocs',
                        action='append_const',
                        dest='funcs',
                        const=parent.get_format_relocations,
                        help='Print relocations of the file')

    # OK
    parser.add_argument('--summary',
                        action='append_const',
                        dest='funcs',
                        const=parent.get_summary,
                        help='Print Summary')

    # OK
    parser.add_argument('--gresources',
                        action='append_const',
                        dest='funcs',
                        const=parent.graphic_resources,
                        help='Opens graphic viewer for looking '
                             'resources')

    parser.add_argument('filename', help="Executable file (exe or dll)")

    return parser
