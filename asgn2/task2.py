from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import SHA256
import os

# Parameters (1024-bit safe prime and generator) (mallory's )
q_hex = ''.join('B10B8F96 A080E01D DE92DE5E AE5D54EC 52C99FBC FB06A3C6\
                9A6A9DCA 52D23B61 6073E286 75A23D18 9838EF1E 2EE652C0\
                13ECB4AE A9061123 24975C3C D49B83BF ACCBDD7D 90C4BD70\
                98488E9C 219A7372 4EFFD6FA E5644738 FAA31A4F F55BCCC0\
                A151AF5F 0DC8B4BD 45BF37DF 365C1A65 E68CFDA7 6D4DA708\
                DF1FB2BC 2E4A4371'.split())
q = int(q_hex, 16)

a_hex = 'A4D1CBD5 C3FD3412 6765A442 EFB99905 F8104DD2 58AC507F\
D6406CFF 14266D31 266FEA1E 5C41564B 777E690F 5504F213\
160217B4 B01B886A 5E91547F 9E2749F4 D7FBD7D3 B9A92EE1\
909D0D22 63F80A76 A6A24C08 7A091F53 1DBF0A01 69B6A28A\
D662A4D1 8E73AFA3 2D779D59 18D08BC8 858F4DCE F97C2A24\
855E6EEB 22B3B2E5'.split()
alpha = int(''.join(a_hex), 16)

# Helper function to generate symmetric key from shared secret
def generate_symmetric_key(shared_secret):
    sha256 = SHA256.new()
    sha256.update(str(shared_secret).encode('utf-8'))
    return sha256.digest()[:16]  # Truncate to 16 bytes

# Alice's Setup
XA = int.from_bytes(get_random_bytes(4), 'big') % q
YA = pow(alpha, XA, q)

# Bob's Setup
XB = int.from_bytes(get_random_bytes(4), 'big') % q
YB = pow(alpha, XB, q)


'''
MITM ATTACK HERE
Mallory intercepts and replaces YA and YB with q 
'''
YA_intercepted = q
YB_intercepted = q

# Alice computes shared secret and symmetric key with intercepted YB
shared_secret_alice = pow(YB_intercepted, XA, q)
k_alice = generate_symmetric_key(shared_secret_alice)

# Bob computes shared secret and symmetric key with intercepted YA
shared_secret_bob = pow(YA_intercepted, XB, q)
k_bob = generate_symmetric_key(shared_secret_bob)

# AES-CBC encryption/decryption setup
iv = get_random_bytes(AES.block_size)  # Initialization vector

# Ensure Alice and Bob have the same symmetric key
assert k_alice == k_bob, "Symmetric keys do not match!"

# Alice sends a message to Bob
cipher = AES.new(k_alice, AES.MODE_CBC, iv)
plaintext = b"Hi Bob, sending secret code!"
ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

# Bob decrypts Alice's message
cipher = AES.new(k_bob, AES.MODE_CBC, iv)
decrypted_msg = unpad(cipher.decrypt(ciphertext), AES.block_size)
print(f"Bob receives and decrypts: {decrypted_msg.decode()}")

# Bob sends a response to Alice
cipher = AES.new(k_bob, AES.MODE_CBC, iv)
plaintext = b"Hi Alice... you are not a spy are you?"
ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

# Alice decrypts Bob's message
cipher = AES.new(k_alice, AES.MODE_CBC, iv)
decrypted_msg = unpad(cipher.decrypt(ciphertext), AES.block_size)
print(f"Alice receives and decrypts: {decrypted_msg.decode()}")

# Tampering with alpha
alpha_tampered = 1  # Mallory sets alpha to 1

# Alice's Setup with tampered alpha
XA = int.from_bytes(get_random_bytes(4), 'big') % q
YA = pow(alpha_tampered, XA, q)

# Bob's Setup with tampered alpha
XB = int.from_bytes(get_random_bytes(4), 'big') % q
YB = pow(alpha_tampered, XB, q)

# Alice computes shared secret and symmetric key with tampered alpha
shared_secret_alice = pow(YB, XA, q)
k_alice = generate_symmetric_key(shared_secret_alice)

# Bob computes shared secret and symmetric key with tampered alpha
shared_secret_bob = pow(YA, XB, q)
k_bob = generate_symmetric_key(shared_secret_bob)

# Ensure Alice and Bob have the same symmetric key
assert k_alice == k_bob, "Symmetric keys do not match!"
