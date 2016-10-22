import sys
import os
from collections import Counter
from preprocessing import has_cue
from transition import compute_transition_probabilities
from viterbi import viterbi, viterbi_again
from sklearn.metrics import f1_score
from constants import DEBUG, SMOOTHED, TRAINING_DIRECTORY, CUES, LOGGING


def compute_emission_probabilities(directory=TRAINING_DIRECTORY, smoothed=SMOOTHED):
    """
    Computes the emission probabilities over the training data.
    Emission prob. key/value example: ("table", "<B-CUE") : 0.015.
    Returns the emission probs dict and the word POS list
    """
    emission_counts = Counter()
    emission_probabilities = dict()
    cue_counts = Counter()
    
    for file in os.listdir(directory):
        data = open("{}/{}".format(directory, file), 'r+')
        for line in data:
            line = line.strip("\n")
            cue = has_cue(line)
            word = line.split("\t")[0].lower()
            if cue:
                cue_counts[cue] += 1
                # Emission count format example : {('students', '<B-CUE>'):3}
                emission_counts[(word, cue)] += 1
            # NULL state has no emission probabilities
            elif "NULL" not in line:
                cue_counts["<O>"] += 1
                emission_counts[(word, "<O>")] += 1
        data.close()
        
    if smoothed:
        emission_counts = smooth_counts(emission_counts)
        # Normalize cue counts with updated smoothed counts
        for cue in cue_counts:
            cue_counts[cue] = sum(emission_counts[(word, cue_tag)] for word, cue_tag in emission_counts
                                  if cue == cue_tag)
            
    for word, tag in emission_counts.iterkeys():
        emission_probabilities[(word, tag)] = float(emission_counts[(word, tag)])/float(cue_counts[tag])
    return emission_probabilities


def compute_gt_count(count, word_counts_inc, word_counts_noninc):
    if word_counts_inc != 0 and word_counts_noninc != 0:
        return (count+1)*float(word_counts_inc)/float(word_counts_noninc)
    else:
        return (count+1)*float(1+word_counts_inc)/float(1+word_counts_noninc)

    
def smooth_counts(counts):
    smoothing_counts = Counter()
    for pair in counts:
        smoothing_counts[counts[pair]] += 1
    for pair, count in counts.copy().iteritems():
        if count < 10:
            word_counts_inc = smoothing_counts[count+1]
            word_counts_noninc = smoothing_counts[count]
            counts[pair] = compute_gt_count(count, word_counts_inc, word_counts_noninc)
            #for cue in CUES:
            #    if counts[(pair[0], cue)] == 0:
            #        counts[(pair[0], cue)] = compute_gt_count(0, word_counts_inc, word_counts_noninc)
    return counts

    
def get_sentences(test_root_dir):
    sentences = []
    for file in os.listdir(test_root_dir):
        curr_sentence = []
        data = open(test_root_dir + file, 'r+')
        for line in data:
            if not line.strip():
                sentences.append(curr_sentence)
                curr_sentence = []
                continue
            else:
                curr_sentence.append(line.split("\t")[0])
        data.close()
    return sentences


def compute_uncertainty_spans(tags):
    """
    Computes the uncertainty span string (e.g. "1 2-4 5 6 8-14 ...")
    from the given BIO tag sequences.
    tags is a list of lists, where each sublist denotes the BIO tags of words
    in a sentence.
    """
    # Compute the uncertainty spans from the tagged sentences
    count = 0
    uncertainty_spans = ""
    
    for sentence in tags:
        in_cue = False
        cue_begin = 0
        cue_end = 0
        for tag in sentence:
            if tag == '<B-CUE>':
                in_cue = True
                cue_begin = count
                cue_end = cue_begin
            elif tag == '<I-CUE>' and in_cue:
                cue_end = count
            elif tag == "<O>" and in_cue:
                uncertainty_spans += "{}-{} ".format(cue_begin, cue_end)
                in_cue = False
            count += 1
    return uncertainty_spans


def find_uncertain_sentences(tags):
    """
    Returns a string with pointers to all sentences containing an 
    uncertain phrase.
    """
    uncertain_sentences = ""
    count = 0
    for sentence in tags:
        if '<B-CUE>' in sentence:
            uncertain_sentences += "{} ".format(count)
        count += 1
    return uncertain_sentences

    
def phrase_sentence_label():
    # Gets a list of public and private sentences from the test data
    public_sentences = get_sentences(os.getcwd() + "/test-public/")
    private_sentences = get_sentences(os.getcwd() + "/test-private/")
    
    public_tags = []
    private_tags = []

    transition = compute_transition_probabilities()
    emission = compute_emission_probabilities()
    
    # Use Viterbi algorithm to determine appropriate cue tags/labels for each sentence
    for sentence in public_sentences:
        public_tags.append(viterbi(emission, transition, sentence))
    for sentence in private_sentences:
        private_tags.append(viterbi(emission, transition, sentence))

    public_uncertainty_spans = compute_uncertainty_spans(public_tags)
    private_uncertainty_spans = compute_uncertainty_spans(private_tags)
    public_uncertain_sentences = find_uncertain_sentences(public_tags)
    private_uncertain_sentences = find_uncertain_sentences(private_tags)
    
    if LOGGING:
        with open('hmm_phrase_classification.csv', 'w+') as file:
            writer = csv.writer(file)
            writer.writerow(['Type', 'Spans'])
            writer.writerow(['CUE-public', public_uncertainty_spans])
            writer.writerow(['CUE-private', private_uncertainty_spans])
        with open('hmm_sentence_classification.csv', 'w+') as file:
            writer = csv.writer(file)
            writer.writerow(['Type', 'Indices'])
            writer.writerow(['SENTENCE-public', public_uncertainty_sentences])
            writer.writerow(['SENTENCE-private', private_uncertainty_sentences])
    return {'public_uncertainty_spans': public_uncertainty_spans,
            'private_uncertainty_spans': private_uncertainty_spans,
            'public_uncertain_sentences': public_uncertain_sentences,
            'private_uncertain_sentences': private_uncertain_sentences}

def compute_F1_score(pred_tags, actual_tags):
    """
    Computes the F1 score between the predicted tags and the actual tags.
    Both inputs are assumed to be a list of lists of tags, where each sub-list corresponds
    to a sentence.
    """
    predictions = sum(pred_tags, [])
    actual = sum(actual_tags, [])
    return f1_score(predictions, actual)

    
def test_emissions():
    # Sanity checks
    emission_probs = compute_emission_probabilities(directory=TRAINING_DIRECTORY)
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
        print "Error: There should not be emission probabiities on the NULL state"

        
def test_viterbi():
    word_pos_list = ['hi','there','i','am','several','turnips']
    transition = compute_transition_probabilities()
    emission = compute_emission_probabilities(directory=TRAINING_DIRECTORY)
    print viterbi(emission, transition, word_pos_list)
    

def main():
    if DEBUG:
        test_emissions()
        test_viterbi()

        
if __name__ == '__main__':
    main()

