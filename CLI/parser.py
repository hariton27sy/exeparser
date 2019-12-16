import argparse


def get_parser(parent):
    usage = ('[-h] [--file-header] [--optional-header]\n\t'
             '[--raw-section-header RAW_SECTION_HEADER] [--headers]\n\t'
             '[--exports] [--imports] [--dependents] [--resources] [--raw]'
             '\n\t[--relocs] [--summary] [--gresources]\n\t'
             'filename\n\t'
             '[--section-headers [SECTION_HEADERS [SECTION_HEADERS ...]]]')
    description = ('This script allow you to check executable windows '
                   'files.\nYou do not to install requirements if you '
                   'use only CLI version')

    parser = argparse.ArgumentParser(description=description,
                                     usage=usage)

    parser.add_argument('--file-header',
                        action='store_const',
                        const=parent.file_header,
                        help='Prints file header of the file')

    parser.add_argument('--optional-header',
                        action='store_const',
                        const=parent.optional_header,
                        help='Prints optional header of the file')

    parser.add_argument('--data-directory-raw', action='store',
                        type=int,
                        help="Print raw dump of data directory which has "
                             "this position")

    parser.add_argument('--section-headers',
                        action='store',
                        nargs='*',
                        default=[-1, -1],
                        type=int,
                        help='Takes from 0 to 2 parameters and'
                             'if 0 parameters print all section info '
                             'if 1 parameter print section info with '
                             'number, if 2 params print from 1 number'
                             ' to 2')

    parser.add_argument('--raw-section-header', action='store',
                        type=int,
                        help='print raw dump section that has position of '
                             'this number in the file')

    parser.add_argument('--full-section-header', action='store',
                        type=int,
                        help='print full information with dump about section '
                             'that has this number')

    parser.add_argument('--headers',
                        action='store_const',
                        const=parent.headers,
                        help='Prints file, optional and section'
                             'headers')

    parser.add_argument('--exports',
                        action='store_const',
                        const=parent.format_export_table,
                        help='Print info about export section of the'
                             'file')

    parser.add_argument('--imports',
                        action='store_const',
                        const=parent.format_import_table,
                        help='Print info about imports of the file')

    parser.add_argument('--dependents',
                        action='store_const',
                        const=parent.format_dependencies,
                        help='Print info about dependencies')

    parser.add_argument('--resources',
                        action='store_const',
                        const=parent.get_format_resources,
                        help='Print resources of the a file')

    parser.add_argument('--raw',
                        action='store_const',
                        const=parent.get_raw_file,
                        help='Print hex dump of the file')

    parser.add_argument('--relocs',
                        action='store_const',
                        const=parent.get_format_relocations,
                        help='Print relocations of the file')

    parser.add_argument('--summary',
                        action='store_const',
                        const=parent.get_summary,
                        help='Print Summary')

    parser.add_argument('--gresources',
                        action='store_const',
                        const=parent.graphic_resources,
                        help='Opens graphic viewer for looking '
                             'resources')

    parser.add_argument('filename')

    return parser
