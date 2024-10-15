from nltk.corpus import words

# Load the words corpus
word_list = words.words()

# Define the file name
file_name = "word_list.txt"

# Write the words to a text file
with open(file_name, "w") as file:
    for word in word_list:
        file.write(word + "\n")

print("Word list saved to", file_name)