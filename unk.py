import os
from sets import Set
from constants import DEBUG, TRAINING_DIRECTORY

# Changes first occurrance of a word to <unk>
def add_unk(directory=TRAINING_DIRECTORY):
    seen_words = Set()
    for file in os.listdir(directory):
        data = open(directory + file, 'r')
        preprocessed_data = open(directory[:-1] + "_unk/" + file, 'w+')
        for line in data:
            if line.strip("\n") and (line.split()[0] != "NULL") and (line.split()[0].lower() not in seen_words):
                preprocessed_data.write(line.replace(line.split()[0], "<unk>", 1))
                seen_words.add(line.split()[0].lower())
            else:
                preprocessed_data.write(line)
        preprocessed_data.close()
        data.close()



def main():
    add_unk()

if __name__ == "__main__":
    main()