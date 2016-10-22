import sys
import os

# We do not make an explicit assumption on whether to keep zero probabilities in
# the dictionary or not.

BIO = {"<B-CUE>": 0, "<I-CUE>": 1, "<O>": 2}

# Precondition: entries of word_POS_list are the observed variables in the
# emission probability
# Return: highest (probability_of_tag_sequence, tag_sequence)
def viterbi(emission_prob, transition_prob, word_POS_list):
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
    #for i in range(len(max_node_prob)):
    #    print(max_node_prob[i])
    #print max_node_prob[len(max_node_prob)-1]
    return(max(max_node_prob[-1], key=lambda t: t[0]))

            
def viterbi_again(emission, transition, word_POS_list):
    path_probs = [[0]*len(word_POS_list)]*len(BIO)
    state_paths = path_probs
    viterbi_path = [0]*len(word_POS_list)
    
    for bio in BIO:
        path_probs[BIO[bio]][0] = transition.get((bio, "NULL"), 0)*emission.get((word_POS_list[0], bio), 0)
        state_paths[BIO[bio]][0] = 0
    
    for i in range(1, len(word_POS_list)):
        for bio in BIO:
            path_probs[BIO[bio]][i] = max(path_probs[BIO[k]][i-1]*transition.get((bio, k), 0)*emission.get((word_POS_list[i], k), 0)
                                          for k in BIO)
            # this is a stupid way to get argmax
            most_likely_path = max(path_probs[BIO[k]][i-1]*transition.get((bio, k), 0) for k in BIO)
            for k in BIO:
                   if path_probs[BIO[k]][i-1]*transition.get((bio, k), 0) == most_likely_path:
                       state_paths[BIO[bio]][i] = BIO[k]
                       break
    most_likely_prob = max(path_probs[BIO[k]][len(word_POS_list)-1] for k in BIO)

    for k in range(len(BIO)):
        if path_probs[k][len(word_POS_list)-1] == most_likely_prob:
            viterbi_path[len(word_POS_list)-1] = k
            break

    for i in range(len(word_POS_list)-1, 0, -1):
        viterbi_path[i-1] = state_paths[viterbi_path[i]][i]
    final_cue_list = []
    for index in viterbi_path:
        for k in BIO:
            if BIO[k] == index:
                final_cue_list.append(k)
    return final_cue_list
                
    
