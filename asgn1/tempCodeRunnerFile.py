    attacked = ciphertext[0:18] + bytes([ciphertext[18] ^ xor]) + ciphertext[19:24] + bytes([ciphertext[24] ^ xor2]) + ciphertext[25:]
