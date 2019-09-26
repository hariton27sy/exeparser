language = 'English'

menu = {}

toolbar = {}

cli_help = '''This script allow you to check executable windows files.

Warning! You need to install requirements only if you want to use graphic version of program

Using:
python *filename.py* [parameters]
  * -g [path_to_file]               Start graphical version of
                                    program. If you put path_to_file
                                    program automatically open it.
                                    Warning! you need installed PyQt5
  * <empty arguments>, --help, -h   Print this message
  * -f path_to_file                 Change file to analysis
  * -a, --all                       Print all information about
                                    file (without tables)'''

main_page = 'In this app you can view information about executable files (.exe).\nTo start open file (Ctrl+O)'

headers_info = ('Headers Info', {
    'file_header': ('File Header',
                    ['Field Name', 'Value', 'Description'],
                    {
                        'machine': 'Machine Type',
                        'numberOfSections': 'Number of Sections',
                        'creatingTime': ('Time Date Stamp', '%d-%b-%Y %H:%M:%S'),
                        'pointerToSymbolTable': 'Pointer to Symbol Table',
                        'numberOfSymbols': 'Number of Symbols',
                        'sizeOfOptionalHeader': 'Size of Optional Header',
                        'characteristics': ('Characteristics', [
                            'Relocation information is stripped from the file',
                            'The file is executable',
                            'Line numbers are stripped from the file',
                            'Local symbols are stripped from the file',
                            'Aggressively trim the working set',
                            'The application can handle addresses larger than 2GB',
                            None,  # This flag is reserved for future
                            'Bytes of word are reversed',
                            'Computer supports 32-bit words',
                            'Debugging information is stored separately in a .dbg file',
                            'If the image is on removable media. copy and run from the swap file',
                            'If the image is on the network, copy and run from the swap file',
                            'The file is a system file such as a driver',
                            'The file is a dynamic link library(DLL)',
                            'File should be run only on a uniprocessor computer',
                            'Bytes of the word are reversed'
                        ])
                    }),

    'optional_header': ('Optional Header',
                        ['Field Name', 'Value', 'Description'],
                        {
                            'magic': 'Magic',
                            'linkerVersion': 'Linker Version',
                            'sizeOfCode': 'Size of Code',
                            'sizeOfInitializedData': 'Size of Initialized data',
                            'sizeOfUninitializedCode': 'Size of Uninitialized data',
                            'addressOfEntryPoint': 'Address of Entry Point',
                            'baseOfCode': 'Base of Code',
                            'baseOfData': 'Base of Data',
                            'imageBase': 'Image Base',
                            'sectionAlignment': 'Section Alignment',
                            'fileAlignment': 'File Alignment',
                            'operatingSystemVersion': 'Operating System Version',
                            'imageVersion': 'Image Version',
                            'subsystemVersion': 'Subsystem Version',
                            'win32VersionValue': 'Win32 Version Value',
                            'sizeOfImage': 'Size of Image',
                            'sizeOfHeaders': 'Size of Headers',
                            'checkSum': 'Checksum',
                            'subsystem': ('Subsystem',
                                          {
                                              1: 'No subsystem required',
                                              2: 'Windows graphical user interface (GUI) subsystem.',
                                              3: 'Windows character-mode user interface (CUI) subsystem.',
                                              5: 'OS/2 CUI subsystem.',
                                              7: 'POSIX CUI subsystem.',
                                              9: 'Windows CE system.',
                                              10: 'Extensible Firmware Interface (EFI) application.',
                                              11: 'EFI driver with boot services.',
                                              12: 'EFI driver with run-time services.',
                                              13: 'EFI ROM image.',
                                              14: 'Xbox system.',
                                              16: 'Boot application.'
                                          }, 'Unknown'),
                            'dllCharacteristics': ('DLL Characteristics', [
                                'Reserved', 'Reserved', 'Reserved', 'Reserved', None, None,
                                'The DLL can be relocated at load time',
                                'Code integrity checks are forced',
                                'The image is compatible with data execution prevention (DEP)',
                                'The image is isolation aware, but should not be isolated.',
                                'The image does not use structured exception handling (SEH). No handlers can be '
                                'called in this image. ',
                                'Do not bind the image.',
                                'Reserved.', 'A WDM Driver', 'Reserved', 'The image is terminal server aware'
                            ]),
                            'sizeOfStackReserve': 'Size of Stack Reserve',
                            'sizeOfStackCommit': 'Size of Stack Commit',
                            'sizeOfHeapReserve': 'Size of Heap Reserve',
                            'sizeOfHeapCommit': 'Size of Heap Commit',
                            'loaderFlags': None,
                            'numberOfRvaAndSizes': 'Number of Data Directories'
                        })
})

data_directory_tab = ('Data Directory', ['Field name', 'Virtual Address', 'Size'], (
    'Export table',
    'Import table',
    'Resource table',
    'Exception table',
    'Security table',
    'Base Relocation table',
    'Debug table',
    'Copyright table',
    'Architecture specific data',
    'RVA of GP',
    'TLS table',
    'Load Configuration table',
    'Bound Import Directory in headers',
    'Import Address table',
    'Delay Load Import Descriptors',
    'COM Runtime descriptor'
))

section_headers_tab = ('Section Headers',
                       ['Name', 'Virtual Size', 'Virtual Address', 'Size of Raw Data', 'Pointer to Raw Data',
                        'Pointer to Relocations', 'Pointer to Line Numbers', 'Number of Relocations',
                        'Number of Numberlines', 'Characteristics'])
