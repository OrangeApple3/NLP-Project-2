import os
import sys


# python transition.py 
# trans_probability dictionary key ("<B-CUE>", "<I-CUE>") --> p(<B-CUE>|<I-CUE>)

def compute_transition_probabilities():
    transitions = {("<B-CUE>","<B-CUE>"):0, ("<B-CUE>","<I-CUE>"):0, ("<B-CUE>","<O>"):0, ("<I-CUE>", "<B-CUE>"):0, ("<I-CUE>", "<I-CUE>"):0, ("<I-CUE>", "<O>"):0, ("<O>", "<B-CUE>"):0, ("<O>", "<I-CUE>"):0, ("<O>", "<O>"):0, ("NULL", "<B-CUE>"):0, ("NULL", "<I-CUE>"):0, ("NULL", "<O>"):0}
    transitions_p = {("<B-CUE>","<B-CUE>"):0, ("<B-CUE>","<I-CUE>"):0, ("<B-CUE>","<O>"):0, ("<I-CUE>", "<B-CUE>"):0, ("<I-CUE>", "<I-CUE>"):0, ("<I-CUE>", "<O>"):0, ("<O>", "<B-CUE>"):0, ("<O>", "<I-CUE>"):0, ("<O>", "<O>"):0, ("NULL", "<B-CUE>"):0, ("NULL", "<I-CUE>"):0, ("NULL", "<O>"):0}
    all_file_tags = []
    num_b = 0
    num_i = 0
    num_o = 0
    num_n = 0
    for fn in os.listdir("train_preprocessed/"):
        with open("train_preprocessed/" + fn) as train_file:
            file_tags = []
            for line in train_file:
                file_line = line.split()
                if len(file_line) == 0:
                    continue
                file_tags.append(file_line[-1])
                if file_line[-1] == "<B-CUE>":
                    num_b += 1
                if file_line[-1] == "<I-CUE>":
                    num_i += 1
                if file_line[-1] == "<O>":
                    num_o += 1
                if file_line[-1] == "NULL":
                    num_n += 1
        all_file_tags.append(file_tags)
    for tag_list in all_file_tags:
        while len(tag_list) > 1:
            try:
                transitions[(tag_list[0], tag_list[1])] += 1
                tag_list = tag_list[1:]
            except KeyError:
                transitions[(tag_list[0], tag_list[1])] = 1
                tag_list = tag_list[1:]
    for trans in transitions.keys():
        if trans[1] == "<B-CUE>":
            denom = num_b
        if trans[1] == "<I-CUE>":
            denom = num_i
        if trans[1] == "<O>":
            denom = num_o
        if trans[1] == "NULL":
            denom = num_n
        transitions_p[trans] = transitions[trans]/float(denom)
    trans_probability = {}
    for k in transitions_p.keys():
        trans_probability[(k[1],k[0])] = transitions_p[k]
    return trans_probability
