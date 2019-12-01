def hex_from_bytes(byte_str, symbols_len=0):
    if not isinstance(byte_str, (str, bytes, bytearray)):
        raise TypeError

    if isinstance(byte_str, str):
        byte_str = bytes(byte_str)
    if len(byte_str) == 0:
        return ''

    result = hex(int.from_bytes(byte_str, 'little'))[2:].upper()
    if len(result) < symbols_len:
        result = result.zfill(symbols_len)
    if len(result) % 2 == 1 and symbols_len == 0:
        result = '0' + result
    return '0x' + result


def hex_from_number(number, symbols_len=4):
    return '0x' + hex(number)[2:].upper().zfill(symbols_len)


def bytes_line_to_symbols(line):
    """Example of input: \"0A 5B 9F 4D\"
                     or: \"5B0A 4D9F\""""
    if line is None:
        return ''
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


def formatted_output(base_address, data):
    """data can be enumerator of byte"""
    result = ''
    counter = 0
    line = ''
    for i in data:
        if isinstance(i, bytes):
            i = i[0]
        if counter != 0 and counter % 16 == 0:
            yield f'0x{hex(base_address + counter - 16)[2:]:0>8}: ' \
                      f'{line} {bytes_line_to_symbols(line)}\n'
            line = ''
        line += f'{hex(i)[2:].upper():0^2} '
        counter += 1
    if len(line) > 0:
        yield (f'0x{hex(base_address + counter - (counter % 16))[2:]:0>8}:'
               f' {line:48} {bytes_line_to_symbols(line)}\n')

    return result


def get_line(f, address):
    """find and return line that starts with address and ends by zero-byte
    Parameters:
        f - file stream,
        address - raw address of string"""
    temp_address = f.tell()
    f.seek(address, 0)
    letters = []
    let = f.read(1)
    while let != b'' and let != b'\x00':
        letters.append(let)
        let = f.read(1)
    f.seek(temp_address, 0)
    try:
        return b''.join(letters).decode('utf-8')
    except Exception as e:
        return ""
