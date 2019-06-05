def single_char_xor(input_bytes, char_value):
    output_bytes = b''
    for byte in input_bytes:
        output_bytes += bytes([byte ^ char_value])
    return output_bytes

def main():
    ct = bytes.fromhex('7b5a4215415d544115415d5015455447414c155c46155f4058455c5b523f')
    for i in range(0, 256):
        print(single_char_xor(ct, i))

    # output = b'Now that the party is jumping\n'

if __name__ == '__main__':
    main()