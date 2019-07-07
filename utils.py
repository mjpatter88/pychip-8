def byte_to_bits(byte):
    return [
        byte & 0b10000000,
        byte & 0b01000000,
        byte & 0b00100000,
        byte & 0b00010000,
        byte & 0b00001000,
        byte & 0b00000100,
        byte & 0b00000010,
        byte & 0b00000001,
    ]

def sprite_to_bytes(sprite):
    # A sprite is 5 bytes
    bytes = []
    for x in range(5):
        value = (sprite >> x*8) & 0xFF
        bytes.append(value)
    return reversed(bytes)

# https://github.com/mattmikolay/chip-8/wiki/CHIP%E2%80%908-Technical-Reference#fonts
SPRITE_DATA = [
    0xF0909090F0, 0x2060202070, 0xF010F080F0, 0xF010F010F0,
    0x9090F01010, 0xF080F010F0, 0xF080F090F0, 0xF010204040, 
    0xF090F090F0, 0xF090F010F0, 0xF090F09090, 0xE090E090E0,
    0xF0808080F0, 0xE0909090E0, 0xF080F080F0, 0xF080F08080
]