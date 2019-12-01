import struct

from common_funcs import hex_from_number


class RelocationElement:
    def __init__(self, address, relocType):
        self.relocationType = relocType
        self.address = address


class Relocations:
    def __init__(self, rva, sizeOfBlock, relocations):
        self.virtualAddress = rva
        self.sizeOfBlock = sizeOfBlock
        self.relocationsCount = (sizeOfBlock - 8) // 2
        self.relocations = relocations


class RelocationsParser:
    def __init__(self, path, position, size):
        self.relocs = parse_relocations(path, position, size)

    def get_str(self):
        relocTypes = {
            0: 'ABSOULUTE',
            3: 'HIGHLOW'
        }
        result = [f'BASE RELOCATIONS:']
        for relocation in self.relocs:
            result.append(
                f'\t{hex_from_number(relocation.virtualAddress)} RVA '
                f'{relocation.sizeOfBlock} '
                f'SizeOfBlock {relocation.relocationsCount} '
                'Count of relocations')
            for elem in relocation.relocations:
                relocType = relocTypes[elem.relocationType]
                result.append(f'\t\t{hex_from_number(elem.address, 6)} '
                              f'{relocType}')

        return '\n'.join(result)

    def __str__(self):
        return self.get_str()


def parse_relocations(path, position, size):
    if position == 0:
        return None
    result = []
    with open(path, 'rb') as f:
        f.seek(position)
        while f.tell() < position + size:
            rva, blockSize = struct.unpack('II', f.read(8))
            relocsCount = (blockSize - 8) // 2
            relocs = []
            for _ in range(relocsCount):
                data = bin(int.from_bytes(f.read(2), 'little'))[2:].zfill(16)
                relocs.append(RelocationElement(int(data[4:], 2),
                                                int(data[:4], 2)))

            result.append(Relocations(rva, blockSize, relocs))

    return result
