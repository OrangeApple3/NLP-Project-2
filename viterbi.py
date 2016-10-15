import sys
import os

# We do not make an explicit assumption on whether to keep zero probabilities in
# the dictionary or not. 

# Returns highest (probability_of_tag_sequence, tag_sequence)
def viterbi(emission_prob, transition_prob, word_POS_list):
    BIO = {"B": 0, "I": 1, "O": 2}

    max_node_prob = []
    max_node_prob.extend([(0,[]) for _ in range(3)] 
                         for _ in range(word_POS_list))
    
    for curr_BIO in BIO:
        e_prob = emission_prob.get((word_POS_list[0], curr_BIO),0)
        t_prob = transition_prob.get((curr_BIO, "NULL"),0)
        max_node_prob[0][BIO[curr_BIO]] = (e_prob * t_prob, [curr_BIO])

    for curr_word in range(1,len(word_POS_list)):
        for curr_BIO in BIO:
            max_tag_tuple = max(lambda t: transition_prob[t] 
                                if t[0] == curr_BIO else -1, transition_prob)
            e_prob = emission_prob.get((word_POS_list[curr_word], curr_BIO),0)
            t_prob = transition_prob.get((curr_BIO, max_tag_tuple[1]),0)

            max_node_prob[curr_word][BIO[curr_BIO]] = (
                    max_node_prob[curr_word-1][BIO[curr_BIO]][0] 
                    *  e_prob * t_prob,
                    # Appending most probable BIO tag
                    max_node_prob[curr_word-1][BIO[max_tag_tuple[1]]][1]
                    + [curr_BIO]
            )
    return(max_node_prob[-1])


def main():
    pass


if __name__ == "__main__":
    main()