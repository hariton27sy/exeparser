language = 'English'

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
                            'dllCharacteristics': ('DLL Characteristics',),
                            'sizeOfStackReserve': 'Size of Stack Reserve',
                            'sizeOfStackCommit': 'Size of Stack Commit',
                            'sizeOfHeapReserve': 'Size of Heap Reserve',
                            'sizeOfHeapCommit': 'Size of Heap Commit',
                            'loaderFlags': None,
                            'numberOfRvaAndSizes': 'Number of Data Directories'
                        })
})
