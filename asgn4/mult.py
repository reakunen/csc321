'''
Use Cal Poly Servers
Instructions: 
ssh username@127x02.csc.calpoly.edu 

Computer used: 
model name: AMD Ryzen Threadripper 3990X 64-Core Processor, 
128 cores 

'''

import bcrypt
import multiprocessing as mp 
import time
import csv
import sys

def load_word_list(file_name):
    with open(file_name, "r") as file:
        word_list = [line.strip() for line in file]
    return word_list

'''Gets the users from the text file'''
def load_users(file_path):
    users = {}
    with open(file_path, 'r') as file:
        for line in file:
            start = line.find(':')
            username = line[:start] 
            user_info = line.strip().split('$')
            salt = user_info[3][:22]
            hash_value = user_info[3][22:]
            whole = line[start+1:].encode().strip()
            users[username] = {
                'algorithm': user_info[1],
                'workfactor': user_info[2],
                'salt': salt,
                'hash': hash_value,
                'whole': whole 
            }
    return users

def write_to_csv(output, file_name):
    with open(file_name, 'w', newline='') as file:
        fieldnames = ['username', 'password', 'time (seconds)', 'workfactor']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in output:
            writer.writerow(row)

def check_password(hashed, word_list, start, end, result, flag):
    for i in range(start, end):
            if flag.value == 1: 
                return 
            word = word_list[i]
            if 6 <= len(word) <= 10:
                encoded_word = word.encode()
                if bcrypt.hashpw(encoded_word, hashed) == hashed:
                    result.put(word)
                    flag.value = 1 
                    return word
    return None

if __name__ == "__main__":
    # Load the word list first 
    words = "words.txt"
    word_list = load_word_list(words)
    # Load the users
    users = load_users("all.txt")
    output = []
    output_file = 'cracked.csv'
    num_processes = mp.cpu_count()  # Get the number of CPU cores
    chunk_size = len(word_list) // num_processes  # Divide word list into chunks
    for username, user_info in users.items():
        processes = []
        hashed = user_info['whole']
        start_time = time.time()
        result = mp.Queue()
        flag = mp.Value('i', 0)
        for i in range(num_processes):
            start = i * chunk_size
            end = start + chunk_size if i < num_processes - 1 else len(word_list)
            process = mp.Process(target=check_password, args=(hashed, word_list, start, end, result, flag))
            processes.append(process)

        for process in processes:
            process.start()
        
        for process in processes:
            process.join()
        end_time = time.time()
        total_time = end_time - start_time
        # export 
        out = {'username': username, 'password': result.get(), 'time': total_time, 'workfactor': user_info['workfactor'] } 
        print(out)
        output.append(out)
        
    write_to_csv(output, output_file)
    print("Output saved to", output_file)