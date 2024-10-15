import random, time, string
import matplotlib.pyplot as plt
from Crypto.Hash import SHA256

def hash(inputStr):
    hashObject = SHA256.new(data=bytes(inputStr, encoding='utf-8'))
    return hashObject.hexdigest()

def hashInput():
    tbhashed = input("Type something to get hashed: ")
    hashObject = SHA256.new(data=bytes(tbhashed, encoding='utf-8'))
    
    #make new string with hamming distance of 1 based on input
    hamArray = bytearray(tbhashed, 'utf-8')
    #00000001
    hamArray[0] ^= (1 << 0)
    hamString = hamArray.decode('utf-8')
    hamObject = SHA256.new(data=bytes(hamString, encoding='utf-8'))

    print('Input Digest in Hex: ', hashObject.hexdigest())
    print('Other Digest in Hex: ', hamObject.hexdigest())

def truncate(digest, bitLen):
    hexLen = bitLen // 4
    remaining = bitLen % 4
    if remaining == 0:
        trunDigest = digest[:hexLen]
        return trunDigest
    else:
        lastHexFull = digest[hexLen]
        lastDecFull = int(lastHexFull, 16)

        trunDec = lastDecFull >> 2
        #get rid of 0x
        return digest[:hexLen] + hex(trunDec)[2:]

def strGen(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def collision(bitLen):
    hashes = {}
    count = 0
    start = time.time()
    while True:
        count += 1
        randomStr = strGen()
        digest = hash(randomStr)
        trunDigest = truncate(digest, bitLen)
        if trunDigest in hashes:
            end = time.time() - start
            return count, end
        hashes[trunDigest] = randomStr

def collisionPlot():
    digestSizes = range(8, 52, 2)
    countResults = []
    timeResults = []

    for size in digestSizes:
        count, time = collision(size)
        countResults.append(count)
        timeResults.append(time)
        print(f"size {size}, {count} attempts, {time: .2f} seconds")

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(digestSizes, timeResults, marker='o')
    plt.title('Digest Size vs. Collision Time')
    plt.xlabel('Digest Size (bits)')
    plt.ylabel('Collision Time (seconds)')

    plt.subplot(1, 2, 2)
    plt.plot(digestSizes, countResults, marker='o', color='red')
    plt.title('Digest Size vs. Number of Inputs to Find Collision')
    plt.xlabel('Digest Size (bits)')
    plt.ylabel('Number of Inputs')

    plt.tight_layout()
    plt.show()

def main():
    collisionPlot()
if __name__ == '__main__':
    main()