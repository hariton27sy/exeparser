def hex_from_bytes(byte_str):
    return '0x' + hex(int.from_bytes(byte_str, 'little'))[2:].upper()