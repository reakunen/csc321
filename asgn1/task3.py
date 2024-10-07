import numpy as np
import matplotlib.pyplot as plt

# Data for AES throughput
aes_key_sizes = [128, 192, 256]
block_sizes = [16, 64, 256, 1024, 8192]
aes_throughput = np.array([
    [373616.00, 344353.38, 348042.77, 346964.15, 346491.44],
    [324354.06, 294535.11, 297789.81, 297318.86, 298566.91],
    [284423.09, 258587.49, 257018.81, 260362.21, 260256.71]
])

# Data for RSA throughput
rsa_key_sizes = [512, 1024, 2048, 4096]
rsa_sign_throughput = np.array([7938.3, 2507.8, 599.3, 89.5]) / 1024  # Convert to kilobytes/s
rsa_verify_throughput = np.array([259767.6, 124691.8, 40992.2, 10784.5]) / 1024  # Convert to kilobytes/s

# Plot AES throughput
plt.figure(figsize=(10, 6))
for i, aes_key_size in enumerate(aes_key_sizes):
    plt.plot(block_sizes, aes_throughput[i], label=f"AES-{aes_key_size} CBC")
plt.title("AES Throughput vs. Block Size")
plt.xlabel("Block Size (bytes)")
plt.ylabel("Throughput (kbytes/s)")
plt.legend()
plt.grid(True)
plt.xscale('log')
plt.xticks(block_sizes, block_sizes)
plt.tight_layout()
plt.show()

# Plot RSA throughput
plt.figure(figsize=(10, 6))
plt.plot(rsa_key_sizes, rsa_sign_throughput, label="RSA Sign")
plt.plot(rsa_key_sizes, rsa_verify_throughput, label="RSA Verify")
plt.title("RSA Throughput vs. Key Size")
plt.xlabel("Key Size (bits)")
plt.ylabel("Throughput (kbytes/s)")  # Updated the ylabel
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
