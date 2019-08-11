# You need to add your file in __init__.py to make visible your language in the program
# Variable language is name of language in interface
# Variable menu is names of menu buttons
# Some positions require additional parameters for


language = 'English'

file_header = ('File header',
               {
                   'machine': ('Architecture',),
                   'numberOfSections': ('Number of Sections', '{0}'),
                   'creatingTime': ('Time Date Stamp', '{0}:"dd.MM.yyyy hh\\:mm\\:ss"'),
                   'pointerToSymbolTable': ('Pointer to Symbol Table', '{0}'),
                   'numberOfSymbols': None,
                   'sizeOfOptionalHeader': None,
                   'characteristics': None
               })

file_header_characteristics = ['Relocation information is stripped from the file',
                               'The file is executable',
                               'Line numbers are stripped from the file',
                               'Local symbols are stripped from the file',
                               'Aggressively trim the working set',
                               'The application can handle addresses larger than 2GB',
                               'Use of this flag is reserved for future use',
                               'Bytes of word are reversed',
                               'Computer supports 32-bit words',
                               'Debugging information is stored separately in a .dbg file',
                               'If the image is on removable media. copy and run from the swap file',
                               'If the image is on the network, copy and run from the swap file',
                               'The file is a system file such as a driver',
                               'The file is a dynamic link library(DLL)',
                               'File should be run only on a uniprocessor computer',
                               'Bytes of the word are reversed']
optional_header = {
    'magic': None,
    'majorLinkerVersion': None,
    'minorLinkerVersion': None,
    'sizeOfCode': None,
    'sizeOfInitializedData': None,
    'sizeOfUninitializedCode': None,
    'addressOfEntryPoint': None,
    'baseOfCode': None,
    'baseOfData': None,
    'imageBase': None,
    'sectionAlignment': None,
    'fileAlignment': None,
    'majorOperatingSystemVersion': None,
    'minorOperatingSystemVersion': None,
    'majorImageVersion': None,
    'minorImageVersion': None,
    'majorSubsystemVersion': None,
    'minorSubsystemVersion': None,
    'win32VersionValue': None,
    'sizeOfImage': None,
    'sizeOfHeaders': None,
    'checkSum': None,
    'subsystem': None,
    'dllCharacteristics': None,
    'sizeOfStackReserve': None,
    'sizeOfStackCommit': None,
    'sizeOfHeapReserve': None,
    'sizeOfHeapCommit': None,
    'loaderFlags': None,
    'numberOfRvaAndSizes': None
}
