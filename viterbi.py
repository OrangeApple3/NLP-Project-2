import sys
import os


# Returns highest (probability_of_tag_sequence, tag_sequence)
def viterbi(emission_prob, transition_prob, word_POS_list):
    BIO = ["B": 0, "I": 1, "O": 2]

    max_node_prob = []
    max_node_prob.extend([(0,[]) for _ in range(3)] for _ in range(word_POS_list))
    
    for curr_BIO in BIO:
        max_node_prob[0][BIO[curr_BIO]] = (
                emission_prob[(word_POS_list[0], curr_BIO)] 
                * transition_prob[(curr_BIO, "NULL")], 
                [curr_BIO]
        )


    for curr_word in range(1,len(word_POS_list)):
        for curr_BIO in BIO:
            max_tag_tuple = max(lambda t: transition_prob[t] 
                                if t[0] == curr_BIO else -1, transition_prob)
            max_node_prob[curr_word][BIO[curr_BIO]] = (
                    max_node_prob[curr_word-1][BIO[curr_BIO]][0] 
                    * emission_prob[(word_POS_list[curr_word], curr_BIO)] 
                    * transition_prob[(curr_BIO, max_tag_tuple[1])],
                    # Appending most probable BIO tag
                    max_node_prob[curr_word-1][BIO[max_tag_tuple[1]]][1]
                    + [max_tag_tuple[0]]
            )
    return(max_node_prob[-1])


def main():
    pass


if __name__ == "__main__":
    main()