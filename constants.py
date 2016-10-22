import os

# Represents HMM states
CUES = ['<B-CUE>', '<I-CUE>', '<O>']

# Change this to change the training directory used for the HMM. Include appropriate Foward Slashes
TRAINING_DIRECTORY = os.getcwd() + "/resampled_unk/"

# Setting this to True will apply Good-Turing smoothing to the emission counts
SMOOTHED = True

# Setting this to True will cause debugging tests to be run
DEBUG = True

# Setting this to be True will cause phrase/sentence classification CSVs to be generated during sequence tagging
LOGGING = True
