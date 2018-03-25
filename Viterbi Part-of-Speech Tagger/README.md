Introduction
For this assignment, you must train a Hidden Markov Model (HMM) on a furnished pre-labeled corpus, and then use the Viterbi algorithm to find the most likely part-of-speech (POS) tags for all the tokens in a separate test document. The corpus and test documents will be tokenized, but you will need to convert all tokens to lower case before processing.  Only primitive lemmatizing will be required, as described below. The corpus and test document file names will be furnished to the program as command arguments. Your program must input the corpus and test documents, build an HMM based on the corpus, and use it to tag the tokens in the test document.  Output must be in the same format as in the provided gold standard output file.

Programming Language
You may use any of the following programming languages:  C, C++, Java, or Python.  You may not use any high-level library functions for constructing the HMM. It is the specific intent of this assignment that you build the HMM yourself using the basic general purpose programming constructs of your chosen programming language. Any use of unauthorized libraries will result in substantial grade deductions.

Your program must run on the instructor's machine, which contains only standard distributions for gcc, g++, Java 8, and Python 3.6.2. You must not require the instructor to install any additional libraries or extensions in order to run your program.

Command Arguments
Your program must accept two command arguments representing, in order, the names of the training corpus and test document files, so that test scripts can be used to run your program on multiple test sets for evaluation.

It is not necessary for your program to do any validation of either the number of arguments or the presence of the named files.  All invocations of your program will be well formed.

Corpus File Format
The corpus file will be a pre-tokenized text file, with one token per line, followed by whitespace and the pre-labeled tag for the token, to be used for training.  Sentence boundaries are indicated by empty lines in the file. You must convert all tokens in this file to lower case before training.

Test File Format
The test file will be a pre-tokenized text file, with one sentence (not token) per line. This file will not be pre-labeled.  Sentence boundaries are indicated by newlines. You must convert all tokens in this file to lower case before testing.

It is possible that the test file may contain some tokens that were not seen in the training corpus.  In this situation, your program should simply tag each such token as NN (common noun). This should allow your Viterbi implementation to proceed with such tokens in the document.

Lemmatizing the Input
In addition to converting all input tokens (but not POS tags) to lower case, only the following primitive lemmatizing for handling plural word forms is required:

If the lower case word ends with "sses" or "xes", then drop the last 2 characters;
Else if it ends with "ses" or "zes", then drop only the last character;
Else if it ends with"ches" or "shes", then drop the last 2 characters;
Else if it ends with "men", then change the last 2 characters to "an";
Else if it ends with "ies", then drop the last 3 characters and add "y".
