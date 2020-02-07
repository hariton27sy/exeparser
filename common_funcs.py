def hex_from_bytes(byte_str, symbols_len=0):
    if not isinstance(byte_str, (str, bytes, bytearray)):
        raise TypeError

    if isinstance(byte_str, str):
        byte_str = bytes(byte_str)
    if not byte_str:
        return ''

    result = hex(int.from_bytes(byte_str, 'little'))[2:]\
        .upper().zfill(symbols_len)
    if len(result) % 2 == 1 and symbols_len == 0:
        result = '0' + result
    return '0x' + result


def hex_from_number(number, symbols_len=4):
    return f"0x{number:0>{symbols_len}X}"


def parse_hex(s):
    n = int(s, 16)
    return chr(n) if 62 < n < 127 else '.'


def bytes_line_to_symbols(line):
    """Example of input: \"0A 5B 9F 4D\"
                     or: \"5B0A 4D9F\""""
    if not line:
        return ''
    temp = []
    chars = line.split(' ')
    for char in chars:
        count = len(char) // 2
        for i in range(count):
            temp.append(char[(count - i - 1) * 2:(count - i) * 2])

    return ''.join(map(parse_hex, temp))


def formatted_output(base_address, data):
    """data can be enumerator of byte"""
    line = ''
    counter = 0
    for counter, e in enumerate(data):
        if isinstance(e, bytes):
            e = e[0]
        if counter != 0 and counter % 16 == 0:
            yield f'0x{hex(base_address + counter - 16)[2:]:0>8}: ' \
                      f'{line} {bytes_line_to_symbols(line)}\n'
            line = ''
        line += f'{hex(e)[2:].upper():0>2} '
    if line:
        yield (f'0x{hex(base_address + counter - (counter % 16))[2:]:0>8}:'
               f' {line:48} {bytes_line_to_symbols(line)}\n')


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


def get_resource_type(data):
    if list_starts_with_second_list(data, [137, 80, 78, 71, 13, 10, 26]):
        return "image"

    return "unknown"


def get_bmp_with_header(data):
    header_size = int.from_bytes(data[0:4], 'little')
    field_size = 2
    if header_size > 12:
        field_size = 4

    pixels_count = int.from_bytes(data[6 + field_size * 2:8 + field_size * 2],
                                  'little')
    pixels_size = (2 ** pixels_count) * 4

    data_position = (14 + header_size + pixels_size).to_bytes(4, 'little')

    size = (14 + len(data)).to_bytes(4, 'little')
    header = b"BM" + size + b"\x00\x00\x00\x00" + data_position

    return header + data


def get_strings_from_data(data, encoding='utf-16'):
    # Внимание костыль
    symbol_length = len("e".encode(encoding))
    if encoding == 'utf-16':
        symbol_length = 2

    pos = 2
    string_length = int.from_bytes(data[0:2], 'little')
    while pos + string_length * symbol_length + 2 < len(data):
        yield data[pos:pos + string_length * symbol_length].decode(encoding)
        pos += string_length * symbol_length + 2
        string_length = int.from_bytes(data[pos-2:pos], 'little')


def list_starts_with_second_list(first_list, second_list):
    for (a, b) in zip(first_list, second_list):
        if a != b:
            return False

    return True
