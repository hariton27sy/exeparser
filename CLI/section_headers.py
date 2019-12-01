from common_funcs import hex_from_bytes


class SectionHeaders:
    def __init__(self, exeFile, lang, args):
        self.lang = lang
        self.exeFile = exeFile
        self.args = args

    def __str__(self):
        localisation = self.lang.section_headers_tab[1]
        sections = self.exeFile.section_headers
        if len(self.args) == 0:
            args = range(0, int(self.exeFile.file_header
                                ['numberOfSections'][1]))
        elif len(self.args) == 2:
            args = range(self.args[0] - 1, self.args[1])
        else:
            args = list(map(lambda x: x - 1, self.args))
        result = []
        for section_number in args:
            if (section_number > int(self.exeFile.file_header
                                     ['numberOfSections'][1])
                    or section_number < 0):
                continue
            temp = ''
            if section_number >= len(sections):
                break
            temp += f'SECTION HEADER #{section_number + 1}\n'
            line_index = 0
            for line in sections[section_number]:
                field = hex_from_bytes(
                    sections[section_number][line]) if line != 'name' else \
                    sections[section_number][line]
                temp += f'{field:>12} {localisation[line_index]}\n'
                line_index += 1
            result.append(temp)

        return '\n'.join(result)
