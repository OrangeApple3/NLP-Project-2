import sys
import os
from collections import Counter
from preprocessing import has_cue


def compute_emission_probabilities(smoothed=False):
    """
    Computes the emission probabilities over the training data.
    Emission prob. key/value example: ("table", "<B-CUE") : 0.015
    """
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
                emission_counts[(line.split("\t")[0].lower(), cue)] += 1
            # NULL state has no emission probabilities
            elif "NULL" not in line:
                cue_counts["<O>"] += 1
                emission_counts[(line.split("\t")[0].lower(), "<O>")] += 1
    for word, tag in emission_counts.iterkeys():
        emission_probabilities[(word, tag)] = float(emission_counts[(word, tag)])/float(cue_counts[tag])
    return emission_probabilities

# Sanity check
emission_probs = compute_emission_probabilities()
sorted_probs = sorted(emission_probs, key=emission_probs.get, reverse=True)

b_cue_probs = [pair for pair in sorted_probs if pair[1] == '<B-CUE>']
# More sanity checks
print "Total B emission probs is " + str(sum(emission_probs[pair] for pair in b_cue_probs))
print "Total I emission probs is " + str(sum(emission_probs[pair] for pair in emission_probs if pair[1] == '<I-CUE>'))
print "Total O emission probs is " + str(sum(emission_probs[pair] for pair in emission_probs if pair[1] == '<O>'))

print "Top five most common beginning cue words"
for i in range(5):
    print "Beginning cue {} has emission probability {}".format(b_cue_probs[i][0], emission_probs[b_cue_probs[i]])
                
            
            
        
    
    
