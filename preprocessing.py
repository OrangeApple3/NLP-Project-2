import os
from sets import Set
import csv

# Note to the graders: To save computation, I generated a separate directory of preprocessed training documents. Several functions
# in this file will not work without it. To replicate this, create a directory within the NLP-Project-2 directory called
# 'train_preprocessed' and run the preprocess function within this module

def has_cue(line):
    # Used for preprocessing - determines if a line has a CUE, returns None if not
    words = line.split("\t")
    try:
        return next(word for word in words if 'CUE' in word)
    except StopIteration:
        return None
    

def preprocess():
    # Preprocesses the data using BIO parsing. Note: this should be run in the nlp-project2-uncertainty directory
    for file in os.listdir(os.getcwd() + "/train"):
        data = open(os.getcwd() + "/train/" + file, 'r+')
        preprocessed_data = open(os.getcwd() + "/train_preprocessed/" + file, 'w+')
        preprocessed_data.write("NULL\n")
        cue = None
        beginning = True
        for line in data:
            line = line.strip("\n")
            if not line.strip():
                preprocessed_data.write(line+"\n")
                preprocessed_data.write("NULL\n")
                continue
            line_cue = has_cue(line)
            if line_cue:
                if cue != line_cue:
                    beginning = True
                if beginning:
                    preprocessed_data.write(line.replace(line_cue, "<B-CUE>") + "\n")
                    beginning = False
                else:
                    preprocessed_data.write(line.replace(line_cue, "<I-CUE>") + "\n")
                cue = line_cue
            else:
                preprocessed_data.write(line + " <O>\n")
                beginning = True
        data.close()
        

def get_uncertain_phrases():
    # Returns a list of uncertain strings from the preprocessed data
    uncertain_phrases = []
    for file in os.listdir(os.getcwd() + "/train_preprocessed"):
        data = open(os.getcwd() + "/train_preprocessed/" + file, 'r+')
        for line in data:
            if '<B-CUE>' in line:
                uncertain_phrases.append(line.split("\t")[0])
    # Remove duplicates
    return Set([phrase.lower() for phrase in uncertain_phrases if len(phrase) >= 4])
    

def baseline_phrase_detection():
    # Uncertainty phrase detection in the test data using the baseline model
    # Note: this naively only considers single words as uncertain as opposed to spans/groups of words
    count = 0
    public_ids = []
    private_ids = []
    uncertain_phrases = get_uncertain_phrases()
    for file in os.listdir(os.getcwd() + "/test-public/"):
        data = open(os.getcwd() + "/test-public/" + file, 'r+')
        for line in data:
            if line.strip():
                # Check if the line contains an uncertain phrase
                if any(phrase for phrase in uncertain_phrases if phrase in line.lower()):
                    public_ids.append("{}-{}".format(count, count))
                count += 1
    count = 0
    for file in os.listdir(os.getcwd() + "/test-private/"):
        data = open(os.getcwd() + "/test-private/" + file, 'r+')
        for line in data:
            if line.strip():
                if any(phrase for phrase in uncertain_phrases if phrase in line.lower()):
                    private_ids.append("{}-{}".format(count, count))
                count += 1
    return ' '.join(public_ids), ' '.join(private_ids)


def baseline_sentence_detection():
    # Identify uncertain sentences in the test data
    count = 0
    public_ids = []
    private_ids = []
    uncertain_phrases = get_uncertain_phrases()
    for file in os.listdir(os.getcwd() + "/test-private"):
        data = open(os.getcwd() + "/test-private/" + file, 'r+')
        for line in data:
            if not line.strip():
                count += 1
            if any(phrase for phrase in uncertain_phrases if phrase in line.lower()) and count not in private_ids:
                private_ids.append(count)
    count = 0
    for file in os.listdir(os.getcwd() + "/test-public"):
        data = open(os.getcwd() + "/test-public/" + file, 'r+')
        for line in data:
            # Sentence delimiters are empty lines
            if not line.strip():
                count += 1
            # Check if sentence contains an uncertain phrase and has not already been recorded
            if any(phrase for phrase in uncertain_phrases if phrase in line.lower()) and count not in public_ids:

                public_ids.append(count)
    public_ids = [str(id) for id in public_ids]
    private_ids = [str(id) for id in private_ids]
    return " ".join(public_ids), " ".join(private_ids)

def uncertainty_phrase_csv():
    public_ids, private_ids = baseline_phrase_detection()
    with open('baseline_phrases.csv', 'w+') as file:
        writer = csv.writer(file)
        writer.writerow(['Type', 'Spans'])
        writer.writerow(['CUE-public', public_ids])
        writer.writerow(['CUE-private', private_ids])

def uncertainty_sentence_csv():
    public_ids, private_ids = baseline_sentence_detection()
    with open('baseline_sentences.csv', 'w+') as file:
        writer = csv.writer(file)
        writer.writerow(['Type', 'Indices'])
        writer.writerow(['SENTENCE-public', public_ids])
        writer.writerow(['SENTENCE-private', private_ids])

preprocess()

