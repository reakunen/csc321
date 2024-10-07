from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import os, sys

''' Reads from a file in binary '''
def read_file(input_file):
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    return plaintext 

''' Writes to file in Binary '''
def write_file(output_file, data): 
    with open(output_file, 'wb') as f: 
        f.write(data)

''' Pads the data with block size's amount in bytes '''
def pkcs7_pad(data, block_size):
    padding_size = block_size - (len(data) % block_size)
    padding = bytes([padding_size] * padding_size)
    return data + padding

''' Encrypts file using ECB or CBC Encryption'''
def encrypt(plaintext, key, iv, mode='ecb'): 
    prev_block = iv

    header = plaintext[:54]
    plaintext = plaintext[54:]
    ciphertext = b'' + header 

    # 16 bytes = 128 bits
    plaintext_pad = pkcs7_pad(plaintext, AES.block_size)

    if mode.lower() == 'ecb': 
        cipher = AES.new(key, AES.MODE_ECB)

        for i in range(0, len(plaintext_pad), AES.block_size):
            block = plaintext_pad[i : i + AES.block_size]
            encrypted_block = cipher.encrypt(block)
            ciphertext += encrypted_block
    elif mode.lower() == 'cbc':
        cipher = AES.new(key, AES.MODE_ECB)

        for i in range(0, len(plaintext_pad), AES.block_size):
            block = plaintext_pad[i : i + AES.block_size]
            xor_block = bytes([b1 ^ b2 for b1, b2 in zip(block, prev_block)])
            encrypted_block = cipher.encrypt(xor_block)
            ciphertext += encrypted_block
            prev_block = encrypted_block

    return ciphertext

def main():
    if len(sys.argv) != 2:
        raise Exception("Usage: python {} <file.bmp>".format(sys.argv[0]))

    input_bmp = sys.argv[1] 
    ecb_output = input_bmp.split('.')[0] + '_ecb.bmp'
    cbc_output = input_bmp.split('.')[0] + '_cbc.bmp'
    print("Generating [{}], [{}] ...".format(ecb_output, cbc_output))
    
    plaintext = read_file(input_bmp)
    key = get_random_bytes(16)  # Generate a random 16-byte (128-bit) key
    iv = get_random_bytes(16)

    ciphertext = encrypt(plaintext, key, iv, 'cbc')
    write_file(cbc_output, ciphertext)
    
    ciphertext = encrypt(plaintext, key, iv, 'ecb')
    write_file(ecb_output, ciphertext)

    print("Finished.")

if __name__ == "__main__":
    main()
