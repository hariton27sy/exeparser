from common_funcs import hex_from_bytes


class FileHeader:
    def __init__(self, exe_file, lang):
        self.exeFile = exe_file
        self.lang = lang

    def __str__(self):
        file_header_lang = self.lang.headers_info[1]['file_header']
        result = [f'{file_header_lang[0].upper()}:\n']
        for key in self.exeFile.file_header:
            val = self.exeFile.file_header[key]
            interpreted_value = val[1]
            if key == 'creatingTime':
                creating_time = file_header_lang[2]['creatingTime'][
                    1] if isinstance(
                    file_header_lang[2]['creatingTime'], tuple) else val[2]
                interpreted_value = interpreted_value(creating_time)
            if key == 'characteristics':
                flags = interpreted_value
                interpreted_value = ['']
                characteristics = file_header_lang[2]['characteristics'][1]
                for (id_, flag) in enumerate(flags):
                    if flag and characteristics[id_] is not None:
                        interpreted_value.append('\t\t\t{}'.format(
                            characteristics[id_]))
                interpreted_value = "\n".join(interpreted_value)
            else:
                interpreted_value = '| ' + interpreted_value
            key_name = (file_header_lang[2][key][0] if isinstance(
                file_header_lang[2][key], tuple) else
                          file_header_lang[2][key])
            result.append('{0:>16} | {1:<30} {2}'.format(
                hex_from_bytes(val[0]), key_name, interpreted_value))

        return "\n".join(result)
