import bcrypt
from nltk.corpus import words
word_list = words.words()

print(word_list)
password = 'aardvark'.encode()
plaintext = 'aardvark'.encode()
# Hash a password for the first time
# hashed = bcrypt.hashpw(password, bcrypt.gensalt())

# gensalt's log_rounds parameter determines the complexity
# the work factor is 2**log_rounds, and the default is 12
salt = bcrypt.gensalt(12)
# print(salt)
# salt = b'$2b$10$SNcf0WuQNU/V/JIJsfkT'
# salt = b'$2b$10$riLFv8OGd18Wszwo2r3ZOO'
hashed = bcrypt.hashpw(password, salt)

print(len(salt), salt)
print(hashed)

hashed = b'$2b$08$J9FW66ZdPI2nrIMcOxFYI.qx268uZn.ajhymLP/YHaAsfBGP3Fnmq'
print(plaintext) 
# Check that an unencrypted password matches one that has
# previously been hashed
if bcrypt.hashpw(plaintext, hashed) == hashed:
	print (hashed, "Matches!", plaintext) 
else:
	print ("Not a match :(")
	