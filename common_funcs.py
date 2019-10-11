def hex_from_bytes(byte_str):
    return '0x' + hex(int.from_bytes(byte_str, 'little'))[2:].upper()


def bytes_line_to_symbols(line):
    """Example of input: \"0A 5B 9F 4D\"
                     or: \"5B0A 4D9F\""""
    if len(line) == 0:
        return ''
    temp = []
    chars = line.split(' ')
    for char in chars:
        count = len(char) // 2
        for i in range(count):
            temp.append(char[(count - i - 1) * 2:(count - i) * 2])

    def parse_hex(s):
        n = int(s, 16)
        return chr(n) if 62 < n < 127 else '.'

    b = ''.join(map(parse_hex, temp))
    return b


def formatted_output(base_address, data: bytes):
    """data can be enumerator of byte"""
    result = ''
    counter = 0
    line = ''
    for i in data:
        if isinstance(i, bytes):
            i = i[0]
        if counter != 0 and counter % 16 == 0:
            result += f'0x{hex(base_address + counter - 16)[2:]:0>8}: ' \
                      f'{line} {bytes_line_to_symbols(line)}\n'
            line = ''
        line += f'{hex(i)[2:].upper():0^2} '
        counter += 1
    if len(line) > 0:
        result += f'0x{hex(base_address + counter - (counter % 16))[2:]:0>8}: ' \
                  f'{line:48} {bytes_line_to_symbols(line)}\n'

    return result
