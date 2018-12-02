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
