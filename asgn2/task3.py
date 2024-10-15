from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes
from Crypto.Random import get_random_bytes

# RSA Key Generation
def generate_rsa_keypair(bits=2048):
    e = 65537
    p = getPrime(bits // 2)
    q = getPrime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    d = inverse(e, phi)
    return ((e, n), (d, n))

# RSA Encryption
def encrypt_rsa(public_key, plaintext):
    e, n = public_key
    m = bytes_to_long(plaintext)
    c = pow(m, e, n)
    return long_to_bytes(c)

# RSA Decryption
def decrypt_rsa(private_key, ciphertext):
    d, n = private_key
    c = bytes_to_long(ciphertext)
    m = pow(c, d, n)
    return long_to_bytes(m)

# Mallory's attack (modify the ciphertext)
def malleability_attack(public_key, private_key, original_ciphertext):
    e, n = public_key
    d, n = private_key
    k = 2  # Mallory's chosen value
    k_e = pow(k, e, n)
    c_prime = (bytes_to_long(original_ciphertext) * k_e) % n
    s = pow(c_prime, d, n)
    return long_to_bytes(s // k)

# Simulation
public_key, private_key = generate_rsa_keypair()

# Alice's message to Bob
alice_message = b"Hello, Bob!"
print(f"Alice's original message: {alice_message}")

# Alice encrypts the message
alice_ciphertext = encrypt_rsa(public_key, alice_message)
print(f"Alice's encrypted message: {alice_ciphertext}")

# Mallory intercepts and modifies the message
mallory_modified_ciphertext = malleability_attack(public_key, private_key, alice_ciphertext)
print(f"Mallory's modified encrypted message: {mallory_modified_ciphertext}")

# Bob receives and decrypts the message
bob_decrypted_message = decrypt_rsa(private_key, alice_ciphertext)
print(f"Bob receives and decrypts: {bob_decrypted_message}")

# Alice decrypts Mallory's modified message
alice_decrypted_mallory_message = decrypt_rsa(private_key, mallory_modified_ciphertext)
print(f"Alice decrypts Mallory's modified message: {alice_decrypted_mallory_message}")

# Bob's response to Alice
bob_message = b"Hi, Alice!"
print(f"Bob's original message: {bob_message}")

# Bob encrypts the message
bob_ciphertext = encrypt_rsa(public_key, bob_message)
print(f"Bob's encrypted message: {bob_ciphertext}")

# Mallory intercepts and modifies Bob's message
mallory_modified_bob_ciphertext = malleability_attack(public_key, private_key, bob_ciphertext)
print(f"Mallory's modified encrypted message: {mallory_modified_bob_ciphertext}")

# Alice receives and decrypts Bob's message
alice_decrypted_bob_message = decrypt_rsa(private_key, bob_ciphertext)
print(f"Alice receives and decrypts: {alice_decrypted_bob_message}")

# Alice decrypts Mallory's modified message
bob_decrypted_mallory_message = decrypt_rsa(private_key, mallory_modified_bob_ciphertext)
print(f"Bob decrypts Mallory's modified message: {bob_decrypted_mallory_message}")
