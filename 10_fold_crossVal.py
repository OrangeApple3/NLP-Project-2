import os
from constants import DEBUG, TRAINING_DIRECTORY


# Separates training set using k-fold cross validation
# Need to first make [directory]_kfold directory in NLP-Project-2 and then make
# [directory]_kfold/train_[i] and [directory]_kfold/train_[i] directories 
# where 1 <= i <= k
def k_crossVal(directory=TRAINING_DIRECTORY, k=10):
    for i in range(k):
        low = 1+(i*(1186/k)) if i+1 != k else 1 + k*(1186/k) 
        high = (i+1) * (1186/k) if i+1 != k else 1186

        for file in os.listdir(directory)[low-1:high]:
            data = open(directory + file, 'r')
            preprocessed_data = open(directory[:-1] + "_kfold/" + "test_{}/".format(i+1) + file, 'w+')
            for line in data:
                preprocessed_data.write(line)
            preprocessed_data.close()
            data.close()
        
        for file in os.listdir(directory)[:low-1]:
            data = open(directory + file, 'r')
            preprocessed_data = open(directory[:-1] + "_kfold/" + "train_{}/".format(i+1) + file, 'w+')
            for line in data:
                preprocessed_data.write(line)
            preprocessed_data.close()
            data.close()

        for file in os.listdir(directory)[high:]:
            data = open(directory + file, 'r')
            preprocessed_data = open(directory[:-1] + "_kfold/" + "train_{}/".format(i+1) + file, 'w+')
            for line in data:
                preprocessed_data.write(line)
            preprocessed_data.close()
            data.close()



def main():
    k_crossVal(directory=os.getcwd() + "/resampled_unk")

if __name__ == "__main__":
    main()