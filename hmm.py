import sys
import os
from collections import Counter
from preprocessing import has_cue


def compute_emission_probabilities(smoothed=False):
    emission_counts = Counter()
    emission_probabilities = dict()
    cue_counts = Counter()
    for file in os.listdir(os.getcwd() + "/train_preprocessed"):
        data = open(os.getcwd() + "/train_preprocessed/{}".format(file), 'r+')
        for line in data:
            line = line.strip("\n")
            cue = has_cue(line)
            if cue:
                cue_counts[cue] += 1
                # Emission count format example : {('students', '<B-CUE>'):3}
                emission_counts[(line.split("\t")[0], cue)] += 1
            elif "NULL" not in line:
                cue_counts["<O>"] += 1
                emission_counts[(line.split("\t")[0], "<O>")] += 1
    for word, tag in emission_counts.iterkeys():
        emission_probabilities[(word, tag)] = float(emission_counts[(word, tag)])/float(cue_counts[tag])
    return emission_probabilities

emission_probs = compute_emission_probabilities()
sorted_probs = sorted(emission_probs, key=emission_probs.get, reverse=True)
for i in range(5):
    print "({}, {}) has emission probability {}".format(sorted_probs[i][0], sorted_probs[i][1], emission_probs[sorted_probs[i]])
                
            
            
        
    
    
