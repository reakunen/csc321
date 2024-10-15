import bcrypt
import base64
import nltk
import time
import sys 
# Load NLTK word corpus
from nltk.corpus import words
word_list = words.words()

def load_shadow_file(file_path):
    users = {}
    with open(file_path, 'r') as file:
        for line in file:
            start = line.find(':')
            username = line[:start] 
            user_info = line.strip().split('$')
            salt = user_info[3][:22]
            hash_value = user_info[3][22:]
            print(salt)
            print(hash_value)
            whole = line[start+1:].encode()
            users[username] = {
                'algorithm': user_info[1],
                'workfactor': user_info[2],
                'salt': salt,
                'hash': hash_value,
                'whole': whole 
            }
    return users

def crack_passwords(users, word_list, output_file):
    start_time = time.time()
    for username, user_info in users.items():
        hash_value = user_info['whole']
        for word in word_list:
            if 6 <= len(word) <= 10:
                password_encoded = word.encode() 
                if bcrypt.hashpw(password_encoded, hash_value) == hash_value:
                    output_file.write(f"Username: {username}, Password: {word}\n")
                    print(username, " matches with ", word)
                    break 
                else:
                    print(word)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total time taken: {total_time} seconds")
    output_file.write(f"Total time taken: {total_time} seconds\n")


if __name__ == "__main__":
    shadow_file_path = "password.txt"  
    users = load_shadow_file(shadow_file_path)
    crack_passwords(users, word_list)
    with open('cracked.txt', 'w') as output_file:
        crack_passwords(users, word_list, output_file)
    print("hello") 