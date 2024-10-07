from task1 import *
from base64 import b64decode
from base64 import b64encode

def cbc_encrypt_string(plaintext, key, iv):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = b''
    prev_block = iv
    plaintext = pkcs7_pad(plaintext, AES.block_size)

    for i in range(0, len(plaintext), AES.block_size):
        block = plaintext[i:i+AES.block_size]
        xor_block = bytes([b1 ^ b2 for b1, b2 in zip(block, prev_block)])
        encrypted_block = cipher.encrypt(xor_block)
        ciphertext += encrypted_block
        prev_block = encrypted_block

    return ciphertext

    
def decrypt(encrypted, key, iv):   
  cipher = AES.new(key, AES.MODE_CBC, iv)
  decryptedtext = unpad(cipher.decrypt(encrypted), AES.block_size)
  return decryptedtext
#   decryptedtextP = decryptedtext.decode("UTF-8")
#   return decryptedtextP

def submit(key, iv): 
    user_input = str(input("Enter a string: "))
    output = 'userid=456;userdata=' + user_input + ';session-id=31337'
    output = 'userid=456;userdata=123456789012344admin>true;session-id=31337'
    ciphertext = cbc_encrypt_string(output.encode('utf-8'), key, iv)
    return ciphertext

def verify(ciphertext, key, iv ):
    # ciphertext = bytearray(ciphertext) 
    xor = ord('4') ^ ord(';')
    xor2 = ord('=') ^ ord('>')
    print(ciphertext)
    # attacked = ciphertext[0:18] + bytes([ciphertext[18] ^ xor]) + ciphertext[19:]
    attacked = ciphertext[0:18] + bytes([ciphertext[18] ^ xor]) + ciphertext[19:24] + bytes([ciphertext[24] ^ xor2]) + ciphertext[25:]

    decrypted_text = decrypt(attacked, key, iv)
    
    print("Decrypted string:", decrypted_text)

    if b";admin=true;" in decrypted_text:
        print("Admin privileges detected (should never happen).")
        return True
    else:
        print("Admin privileges not detected.")
        return False
    pass 

def main ():
    key = get_random_bytes(16)  # Generate a random 16-byte (128-bit) key
    iv = get_random_bytes(16)
    ciphertext = submit(key, iv)
    print('Encrypted CBC String:', ciphertext) 

    print('-----' * 12)

    print(verify(ciphertext, key, iv ))
    
    pass

if __name__ == "__main__": 
    main()
