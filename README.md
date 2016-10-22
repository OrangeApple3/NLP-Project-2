# NLP-Project-2

Python Files:
baseline.py
    - Deprecated. Refer to preprocessing for new baseline.

preprocessing.py
    - Responsible for computing baseline phrase and sentence. 
    - Use baseline_phrase_detection and baseline_sentence_detection
    - Responsible for adding BIO tags.
    - Use preprocess. 

unk.py 
    - Responsible for replacing first occurrences of words in training set with unk. 
    - Use add_unk with optional [directory] parameter 

resampled.py 
    - Responsible for downsampling and upsampling training data. 
    - By default, duplicates all sentences with uncertain phrases.
    - By default, removes sentences with no uncertain phrases with 50% probability
    - Use main with optional [directory] parameter

10_fold_crossVal.py 
    - Responsible for separating training data using k-Fold Cross Validation
    - Use k_cross_val with optional [directory] parameter

transition.py
    - Responsible for computing transition probabilities.
    - Use compute_transition_probabilities with optional [directory] parameter

hmm.py
    - Responsible for computing emission probabilites and F-1 score. 
    - Use compute_emission_probabilities with optional [directory] and [smoothed] parameters  
    - Use compute_f1_score with [pred_tags] and [actual_tags] parameters

viterbi.py
    - Responsible for computing sequence of most probable tags given emission probabilities, 
      transition probabilities, and word sequence using Viterbi algorithm
    - Use viterbi with parameters [emission_prob], [transition_prob], and [word_POS_list]

constants.py
    - Specifies default optional parameters. 

Further Directions: 
To run the HMM, change your working directory to the directory containing the hmm.py, transition.py, viterbi.py, and the training text subdirectories. The “constants.py” file contains constants that adjust the behavior of the model and debugging output. Running "hmm.py" computes the emission and transition probabilities, and then applies the Viterbi algorithm. If DEBUG in constants.py is set to True, several sanity checks will also be outputted. One can also run "python transition.py" to see additional testing output for the transition probabilities. 

