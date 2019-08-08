# Some variables in the program have value is tuple that has two and more positions.
# These variables have comments.
# Then I use positional arguments in interpretation.
# Yes it's crutch

# Also you need escape colon, because it symbol is used for send formats or


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