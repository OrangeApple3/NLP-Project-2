import sys
import os
from hmm import compute_emission_probabilities
from transition import compute_transition_probabilities

# We do not make an explicit assumption on whether to keep zero probabilities in
# the dictionary or not. 

# Precondition: entries of word_POS_list are the observed variables in the
# emission probability
# Return: highest (probability_of_tag_sequence, tag_sequence)
def viterbi(emission_prob, transition_prob, word_POS_list):
    BIO = {"<B-CUE>": 0, "<I-CUE>": 1, "<O>": 2}

    max_node_prob = []
    max_node_prob.extend([(0,[]) for _ in range(3)] 
                         for _ in range(len(word_POS_list)))
    
    for curr_BIO in BIO:
        e_prob = emission_prob.get((word_POS_list[0], curr_BIO),0)
        t_prob = transition_prob.get((curr_BIO, "NULL"),0)
        max_node_prob[0][BIO[curr_BIO]] = (e_prob * t_prob, [curr_BIO])    

    for curr_word in range(1,len(word_POS_list)):
        for curr_BIO in BIO:
            filtered_tags = filter(lambda t: t[0] == curr_BIO and t[1] != "NULL",
                                   transition_prob)
            
            max_tag_tuple = max(filtered_tags, 
                                key=lambda t: transition_prob.get(t,0) 
                                * max_node_prob[curr_word-1][BIO[t[1]]][0])

            e_prob = emission_prob.get((word_POS_list[curr_word], curr_BIO),0)
            t_prob = transition_prob.get(max_tag_tuple,0)


            max_node_prob[curr_word][BIO[curr_BIO]] = (
                    max_node_prob[curr_word-1][BIO[max_tag_tuple[1]]][0] 
                    *  e_prob * t_prob,
                    # Appending most probable BIO tag
                    max_node_prob[curr_word-1][BIO[max_tag_tuple[1]]][1]
                    + [curr_BIO]
            )
    for i in range(len(max_node_prob)):
        print(max_node_prob[i])
    return(max(max_node_prob[-1], key=lambda t: t[0]))


def main():
    emission_probs, _ =  compute_emission_probabilities()
    word_pos_list=["that", "said", ",", "it", "is", "possible", "that", "the", 
                   "threshold", "of", "originality", "is", "very", "low","."]
    
    trans_probs = compute_transition_probabilities()
    print(viterbi(emission_probs,trans_probs,word_pos_list))


if __name__ == "__main__":
    main()
