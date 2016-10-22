import os
import sys
import random
from preprocessing import has_cue
from constants import DEBUG, TRAINING_DIRECTORY

# Upsamples sentences containing uncertainty cues and downsamples sentences without uncertainty cues


# to run: python resample.py
# given a training directory, duplicates the sentences that contain uncertainty cues
# and, with some probability, removes some sentences that do not contain uncertainty


def main(directory=TRAINING_DIRECTORY):
    # ADJUST DOWNSAMPLE HERE
    remove_prob = 50 # probability out of 100 that a sentence with only <O> tags is removed

    for fn in os.listdir(directory):
        with open(directory + "/" + fn) as train_file:
            uncertain_sentences = [] 
            certain_sentences = []
            sentence = [] 
            uncertain = False
            for line in train_file:
                sentence.append(line)
                if has_cue(line) != None: #sentence has uncertainty
                    uncertain = True
                if line == "NULL\n":
                    if uncertain == True:
                        uncertain_sentences.append(sentence)
                    elif uncertain == False:
                        certain_sentences.append(sentence)
                    sentence = []
                    uncertain = False
            for sent in certain_sentences:
                if random.randint(1,100) <= remove_prob:
                    certain_sentences.remove(sent)
            # ADJUST UPSAMPLE HERE
            uncertain_sentences += uncertain_sentences # to repeat sentences, increment uncertain_sentences

        # write to new file
        file = open("resampled_unk/" + fn, "w") # rename to directory designated to contain resampled training files
        for sent in certain_sentences + uncertain_sentences:
            for token in sent:
                file.write(token)
        file.close

if __name__ == '__main__':
  main()