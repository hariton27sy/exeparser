language = 'English'

menu = {}

toolbar = {}

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
                            'subsystem': 'Subsystem',
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
