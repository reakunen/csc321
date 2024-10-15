from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random

# Function to generate a random prime number
def generate_prime(bits):
    while True:
        p = random.getrandbits(bits)
        if is_prime(p):
            return p

# Function to check if a number is prime
def is_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    for _ in range(k):
        a = random.randint(2, n - 1)
        if pow(a, n - 1, n) != 1:
            return False
    return True

# Function to perform modular exponentiation
def mod_exp(base, exp, mod):
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

# Function to perform Diffie-Hellman Key Exchange
def diffie_hellman(q, alpha):
    # Alice picks a random private key
    XA = random.randint(2, q - 1)
    YA = mod_exp(alpha, XA, q)

    # Bob picks a random private key
    XB = random.randint(2, q - 1)
    YB = mod_exp(alpha, XB, q)

    # Shared secret computation
    s = mod_exp(YB, XA, q)
    # Truncate the shared secret to 16 bytes
    s_bytes = int.to_bytes(s, length=16, byteorder='big')

    # Compute AES key using SHA256
    aes_key = SHA256.new(data=s_bytes).digest()

    return aes_key

# Main function
def main():
    # Parameters
    q = 37
    alpha = 5

    # Perform Diffie-Hellman Key Exchange
    shared_key = diffie_hellman(q, alpha)
    print("Shared Key:", shared_key.hex())

    # Example of using the shared key for AES encryption
    # Initialize AES cipher
    cipher = AES.new(shared_key, AES.MODE_CBC, iv=b'16_byte_iv_here')

    # Encrypt message
    message = "Hi Bob!"
    padded_message = pad(message.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_message)
    print("Encrypted:", ciphertext.hex())

# Execute the main function
if __name__ == "__main__":
    main()
