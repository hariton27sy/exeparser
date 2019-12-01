language = 'Russian'

menu = {}

toolbar = {}

main_page = ('В этом приложении Вы можете увидеть информацию '
             'об исполняемом файле. Чтобы начать откройте файл (Ctrl+O)')

headers_info = ('Информация о заголовках', {
    'file_header': ('Файловый заголовок',
                    ['Название поля', 'Значение', 'Пояснение'],
                    {
                        'machine': 'Тип компьюетра/архитектуры',
                        'numberOfSections': 'Количество секций',
                        'creatingTime': ('Дата создания', '%d-%b-%Y %H:%M:%S'),
                        'pointerToSymbolTable': 'Адрес таблицы символов',
                        'numberOfSymbols': 'Количество символов',
                        'sizeOfOptionalHeader': 'Размер '
                                                'дополнительного заголовка',
                        'characteristics': ('Характеристики', [
                            'Relocation information is stripped from the file',
                            'The file is executable',
                            'Line numbers are stripped from the file',
                            'Local symbols are stripped from the file',
                            'Aggressively trim the working set',
                            'The application can handle '
                            'addresses larger than 2GB',
                            None,  # This flag is reserved for future
                            'Bytes of word are reversed',
                            'Computer supports 32-bit words',
                            'Debugging information is stored '
                            'separately in a .dbg file',
                            'If the image is on removable media. '
                            'copy and run from the swap file',
                            'If the image is on the network, copy and run '
                            'from the swap file',
                            'The file is a system file such as a driver',
                            'The file is a dynamic link library(DLL)',
                            'File should be run only on a '
                            'uniprocessor computer',
                            'Bytes of the word are reversed'
                        ])
                    }),

    'optional_header': ('Дополнительный заголовок',
                        ['Название поля', 'Значение', 'Пояснение'],
                        {
                            'magic': 'Магия',
                            'linkerVersion': 'Версия Линкера',
                            'sizeOfCode': 'Рамер кода',
                            'sizeOfInitializedData':
                                'Размер инициализированной информации',
                            'sizeOfUninitializedCode':
                                'Размер неинициализированной информации',
                            'addressOfEntryPoint': 'Адерс точки входа',
                            'baseOfCode': 'Начало секции кода',
                            'baseOfData': 'Начало секции данных',
                            'imageBase': 'Начало образа',
                            'sectionAlignment': 'Выравнивание секций',
                            'fileAlignment': 'Выравнивание в файле',
                            'operatingSystemVersion':
                                'Версия операционной системы',
                            'imageVersion': 'Версия Image',
                            'subsystemVersion': 'Версия подсистемы',
                            'win32VersionValue': 'Версия Win32',
                            'sizeOfImage': 'Размер образа',
                            'sizeOfHeaders': 'Размер заголовков',
                            'checkSum': 'Контрольная сумма',
                            'subsystem': 'Подсистема',
                            'dllCharacteristics': ('DLL Характеристики',),
                            'sizeOfStackReserve':
                                'Размер зарезервированного Стэка',
                            'sizeOfStackCommit': 'Размер фиксированного Стэка',
                            'sizeOfHeapReserve':
                                'Размер зарезервированной кучи',
                            'sizeOfHeapCommit': 'Размер фиксированной кучи',
                            'loaderFlags': None,
                            'numberOfRvaAndSizes': 'Number of Data Directories'
                        })
})
