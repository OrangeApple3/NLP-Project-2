import sys
import os
from collections import Counter
from sets import Set
from preprocessing import has_cue, DEBUG

CUES = ['<B-CUE>', '<I-CUE>', '<O>']

def compute_emission_probabilities(smoothed=False):
    """
    Computes the emission probabilities over the training data.
    Emission prob. key/value example: ("table", "<B-CUE") : 0.015.
    Returns the emission probs dict and the word POS list
    """
    emission_counts = Counter()
    emission_probabilities = dict()
    cue_counts = Counter()
    word_pos_list = []
    for file in os.listdir(os.getcwd() + "/train_preprocessed"):
        data = open(os.getcwd() + "/train_preprocessed/{}".format(file), 'r+')
        for line in data:
            line = line.strip("\n")
            cue = has_cue(line)
            word = line.split("\t")[0].lower()
            if cue:
                cue_counts[cue] += 1
                # Emission count format example : {('students', '<B-CUE>'):3}
                emission_counts[(word, cue)] += 1
                word_pos_list.append(word)
            # NULL state has no emission probabilities
            elif "NULL" not in line:
                cue_counts["<O>"] += 1
                emission_counts[(word, "<O>")] += 1
                word_pos_list.append(word)
    if smoothed:
        emission_counts = smooth_counts(emission_counts)
        # Normalize cue counts with updated smoothed counts
        for cue in cue_counts:
            cue_counts[cue] = sum(emission_counts[(word, cue_tag)] for word, cue_tag in emission_counts
                                  if cue == cue_tag)
            
    for word, tag in emission_counts.iterkeys():
        emission_probabilities[(word, tag)] = float(emission_counts[(word, tag)])/float(cue_counts[tag])
    return emission_probabilities, Set(word_pos_list)

def smooth_counts(counts):
    smoothing_counts = Counter()
    for pair in counts:
        smoothing_counts[counts[pair]] += 1
    for pair, count in counts.copy().iteritems():
        if count < 10:
            word_counts_inc = smoothing_counts[count+1]
            word_counts_noninc = smoothing_counts[count]
            if word_counts_inc != 0 and word_counts_noninc != 0:
                counts[pair] = (count+1)*float(word_counts_inc)/float(word_counts_noninc)
            else:
                counts[pair] = (count+1)*float(1+word_counts_inc)/float(1+word_counts_noninc)
            for cue in CUES:
                if counts[(pair[0], cue)] == 0:
                    counts[(pair[0], cue)] = 1
    return counts

def test_emissions():
    # Sanity checks
    emission_probs, word_pos_list = compute_emission_probabilities(smoothed=True)
    print "Total number of distinct words: {}".format(len(word_pos_list))
    sorted_probs = sorted(emission_probs, key=emission_probs.get, reverse=True)

    b_cue_probs = [pair for pair in sorted_probs if pair[1] == '<B-CUE>']
    i_cue_probs = [pair for pair in sorted_probs if pair[1] == '<I-CUE>']
    o_probs = [pair for pair in sorted_probs if pair[1] == '<O>']
    null_probs = [pair for pair in sorted_probs if pair[1] == 'NULL']

    # More sanity checks
    print "Total B emission probs is " + str(sum(emission_probs[pair] for pair in b_cue_probs))
    print "Total I emission probs is " + str(sum(emission_probs[pair] for pair in emission_probs if pair[1] == '<I-CUE>'))
    print "Total O emission probs is " + str(sum(emission_probs[pair] for pair in emission_probs if pair[1] == '<O>'))

    print "Top five most common beginning cue words"
    for i in range(5):
        print "Beginning cue '{}' has emission probability {}".format(b_cue_probs[i][0], emission_probs[b_cue_probs[i]])
        print "Inside cue '{}' has emission probability {}".format(i_cue_probs[i][0], emission_probs[i_cue_probs[i]])
        print "Outside word '{}' has emission probability {}".format(o_probs[i][0], emission_probs[o_probs[i]])

    if null_probs:
        print "Error: There should not be emission probabiities ont he NULL state"

if DEBUG:
    test_emissions()
