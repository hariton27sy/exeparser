def hex_from_bytes(byte_str):
    return '0x' + hex(int.from_bytes(byte_str, 'little'))[2:].upper()


def bytes_line_to_symbols(line):
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
        return chr(n) if 62 < n < 127 or n > 160 else '.'

    b = ''.join(map(parse_hex, temp))
    return b
