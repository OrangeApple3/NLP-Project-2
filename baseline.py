import os
import sys


# python3 baseline.py <competition_type> 
# competition_type is span or sentence


def build_wordDict():
    word_dictionary={}
    for fn in os.listdir("train/"):
        with open("train/" + fn) as train_file:
            state = "O" 
            for lines in train_file:
                lines = lines.rstrip()
                if state == "O" and lines != '':
                    state = "B"
                    word, pos, tag = lines.split()
                    word_dictionary[word] = \
                        word_dictionary.get(word,set()).union({(pos, state)})
                elif state == "B":
                    if lines == '':
                        state = "O"
                    else:
                        state = "I"
                        word, pos, tag = lines.split()
                        word_dictionary[word] = \
                            word_dictionary.get(word,set()).union({(pos, state)})
                elif state == "I":
                    if lines == '':
                        state = "O"
                    else:
                        word, pos, tag = lines.split()
                        word_dictionary[word] = \
                            word_dictionary.get(word,set()).union({(pos, state)})    
    return(word_dictionary)

def test_annotate(wordDict, file_type, competition_type):
    if competition_type == "span":
        token_id = -1
        span_list = []
        for fn in os.listdir("test-{}/".format(file_type)):
            with open("test-{}/{}".format(file_type, fn)) as test_file:
                state = "O"
                beginning = 0
                for lines in test_file: 
                    lines = lines.rstrip()
                    token_id = token_id + 1 if lines != '' else token_id
                    if state == "O" and lines != '':
                        word, pos = lines.split()
                        if word in wordDict and (pos,"B") in wordDict[word]:
                            beginning = token_id
                            state = "B"
                    elif state == "B":
                        if lines == '':
                            span_list.append("{}-{}".format(beginning, 
                                                            beginning))
                            state = "O"
                        else:
                            word, pos = lines.split()
                            if word in wordDict and (pos,"I") in wordDict[word]:
                                state = "I"
                            else:
                                span_list.append("{}-{}".format(beginning, 
                                                                beginning))
                                state = "O"
                    elif state == "I":
                        if lines == '':
                            span_list.append("{}-{}".format(beginning, 
                                                            token_id-1))
                            state = "O"
                        else:
                            word, pos = lines.split()
                            if (word not in wordDict) or \
                               ((pos,state) not in wordDict[word]):
                                span_list.append("{}-{}".format(beginning, 
                                                                token_id-1))
                                state = "O"
                if state == "I":
                    span_list.append("{}-{}".format(beginning, token_id-1))
                elif state == "B":
                    span_list.append("{}-{}".format(beginning, beginning))

        print("CUE-{},".format(file_type) + " ".join(span_list))

    elif competition_type == "sentence":
        sentence_id = -1
        sentence_list = []
        for fn in os.listdir("test-{}/".format(file_type)):
            with open("test-{}/{}".format(file_type, fn)) as test_file:
                state = "O"
                for lines in test_file:
                    lines=lines.rstrip()
                    if state == "O" and lines != '':
                        sentence_id += 1
                        word, pos = lines.split()
                        if (len(sentence_list) == 0 or 
                            sentence_list[-1] != str(sentence_id)) and \
                            (word in wordDict and (pos,"B") in wordDict[word]):
                                sentence_list.append(str(sentence_id))
                        state = "I"
                    elif state == "I":
                        if lines == '':
                            state = "O"
                        else:
                            if (len(sentence_list) == 0 or 
                                sentence_list[-1] != str(sentence_id)) and \
                                (word in wordDict and (pos,"B") in wordDict[word]):
                                    sentence_list.append(str(sentence_id))
        print("SENTENCE-{},".format(file_type) + " ".join(sentence_list))


def main(wordDict, competition_type):
    if competition_type == "span":
        print("Type,Spans")
        test_annotate(wordDict, "public", competition_type)
        test_annotate(wordDict, "private", competition_type)
    elif competition_type == "sentence":
        print("Type,Indices")
        test_annotate(wordDict, "public", competition_type)
        test_annotate(wordDict, "private", competition_type)
    

if __name__ == '__main__':
  main(build_wordDict(), sys.argv[1])
