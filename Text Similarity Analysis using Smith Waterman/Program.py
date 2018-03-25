# Programming assigment 1 by Syed Abrar Ahmed
# For running the below program please run the below command preceded by the location where this file is located in command prompt or terminator.
# loacation of file > python NlpPA1.py <source_file_name> <target_file_name>

import sys
import re
import numpy as np
import copy

print("""\nUniversity of Central Florida 
CAP6640 Spring 2018 - Dr. Glinos\n
Text Similarity Analysis by Syed Abrar Ahmed\n""")

source_file = open(sys.argv[1] + ".txt", "r")
target_file = open(sys.argv[2] + ".txt", "r")
source_cont = source_file.read()
target_cont = target_file.read()
print("Source File: ", source_file.name)
print("Target File: ", target_file.name)
#source_cont = "A A A A C C C C T G C G G T T A"
#target_cont = "T T C C A C G G G A A C C A A T C"
#source_cont = "loris ipsem Peter picked one peck's worth of pickled peppers. tempus fugit"
#target_cont = "pachabel Peter Piper picked a peck worth of peppers. carpe diem"
#target_cont = '''Keeping the relentless pressure, the pitch unbearable ... we believe so that you do not pause the questions such as'. They will be on the same plane of exaltation as an actor. They are. These events will be like the tide of Hamlet " This article discusses the famous Hamlet monologue of the main themes of the game. Shakespeare is one of the most famous works of Renaissance literature. The drama of this game comes to problems identified by one family. The problems of the wider community is seen through the eyes, the actions and thought of family members. A ruler has the power, and a lot of actions are related to questions about the nature of that power. Took each is undeniable, despite the fact that her son, and authorities Pulonersi feelings (spirit! "Nothing to do with Bo! You sound like a girl green") and behavior of Ajriasa, despite the fact that his decisions suspicious (first third -). '''
#source_cont = "Ask a Question This essay discusses Hamlet's famous soliloquy in relation to the major themes of the play. Shakespeare's is one of the most familiar works of Renaissance literature. The drama of this play concerns problems as revealed through an individual family. The problems of society at large are seen through the eyes, actions and thoughts of members of that family. A ruler is holding power, and a great deal of the action is related to questions about the nature of that power. The general theme of the play deals with a society that is, or has already gone to pieces.Hamlet1 Another theme of the play is that of revenge. Hamlet must avenge his father's death."
#source_cont = "?Hello'. ,Madam, son's aren't I'm"
#target_cont = "?Hello ,Madam, son's aren't I'm"
print("\nRaw Tokens: ")          # Raw tokens as given in the input text files
print("\tSource> ", source_cont)
print("\tTarget> ", target_cont)
source_file.close()

def norm_lower(text):    # function to convert the text into lowercase
    return text.lower()

source_cont = norm_lower(source_cont)
target_cont = norm_lower(target_cont)

def matcher(match):
    if match.group(1) is not None:
        return '{} '.format(match.group(1))
    else:
        return ' {}'.format(match.group(2))

def norm_alnum(text):
    alnum = re.compile(r'^(\W+)|(\W+)$')
    list_of_text = []
    for word in text.split():
        z = list(filter(bool, alnum.sub(matcher, word).split(' ')))
        if z:
            if len(z) == 1:
                list_of_text.append(''.join(z))
            else:
                if any(y.isalnum() for y in z):
                    for token in z:
                        if not token.isalnum():
                            index = z.index(token)
                            z[index] = ' '.join(token)
                list_of_text.append(' '.join(z))
    return list_of_text

source_cont = ' '.join(norm_alnum(source_cont))
target_cont = ' '.join(norm_alnum(target_cont))


def sub(item):  # Function to check if the word starts or ends with specific alphabet or special character and replacing it with another
    if item.endswith("'s"):
        return item.replace("'s", " 's")
    elif item.endswith("n't"):
        return item.replace("n't", "not")
    elif item.endswith("'m"):
        return item.replace("'m", " am")
    else:
        return item


pieces = []
for piece in source_cont.split():
    a = sub(piece)
    if isinstance(a, tuple):
        for b in a:
            pieces.append(b)
    else:
        pieces.append(a)

source_cont = ' '.join(pieces)

pieces = []
for piece in target_cont.split():
    a = sub(piece)
    if isinstance(a, tuple):
        for b in a:
            pieces.append(b)
    else:
        pieces.append(a)

target_cont = ' '.join(pieces)

print("\nNormalized Tokens: ")
print("\tSource> ", source_cont)

source_cont = source_cont.split()

print("\tTarget> ", target_cont)

target_cont = target_cont.split()

def create_score_matrix(rows, cols):  # Function for creating the score matrix and backtrace matrix
    score_matrix = [[0 for col in range(cols)] for row in range(rows)]
    backtrace = [['' for col in range(cols)] for row in range(rows)]
    maximum_score = 0
    max_position = None
    for i in range(1, rows):
        for j in range(1, cols):
            score = calc_score(score_matrix, i, j)
            if score > maximum_score:
                maximum_score = score
                max_position = (i, j)
            score_matrix[i][j] = score
            backtrace[i][j] = next_dir(score_matrix, i, j, score)
    return score_matrix, max_position, backtrace

def calc_score(matrix, x, y): # Function for calculating the score in the score matrix
    if seq1[x-1] == seq2[y-1]:
        similarity = match
    else:
        similarity = mismatch
    diag_score = matrix[x - 1][y - 1] + similarity
    up_score = matrix[x - 1][y] + gap
    left_score = matrix[x][y - 1] + gap
    return max(0, diag_score, up_score, left_score)

def back_trace(backtrace, start_position): #Function for backtracing
    aligned_seq1 = []
    aligned_seq2 = []
    x, y = start_position
    move = backtrace[x][y]
    while move != '':
        if move == 'DI':
            aligned_seq1.append(seq1[x - 1])
            aligned_seq2.append(seq2[y - 1])
            x -= 1
            y -= 1
        elif move == 'UP':
            aligned_seq1.append(seq1[x - 1])
            aligned_seq2.append('-')
            x -= 1
        else:
            aligned_seq1.append('-')
            aligned_seq2.append(seq2[y-1])
            y -= 1

        move = backtrace[x][y]
    return aligned_seq1[::-1], aligned_seq2[::-1], x, y


def next_dir(score_matrix, x, y, score): # Function for determining the next direction
    if seq1[x-1] == seq2[y-1]:
        similarity = match
    else:
        similarity = mismatch
    diagonal = score_matrix[x - 1][y - 1] + similarity
    up = score_matrix[x - 1][y] + gap
    left = score_matrix[x][y - 1] + gap
    if score == 0:
        return ''
    elif score == up:
        return 'UP'
    elif score == left:
        return 'LT'
    elif score == diagonal:
        return 'DI'
    else:
        raise ValueError('invalid move during traceback')

gap = -1
mismatch = -1
match = 2

seq1 = source_cont
seq2 = target_cont

rows = len(seq1) + 1
cols = len(seq2) + 1

score_matrix, start_position, backtrace = create_score_matrix(rows, cols)
matrix = np.array(score_matrix)
max_v = np.amax(matrix)

def edit_action(seq1_aligned, seq2_aligned):  # Function for appending i, s or d as edit action
    alignment_action = []
    for base1, base2 in zip(seq1_aligned, seq2_aligned):
        if base1 == base2:
            alignment_action.append(' ')
        elif base1 == '-':
            alignment_action.append('i')
        elif base2 == '-':
            alignment_action.append('d')
        else:
            alignment_action.append('s')
    return alignment_action

def printing(source_cont, target_cont, table): # Function for printing the matrix and bactrace
    symbol = "#"
    source_cont = [symbol] + source_cont
    target_cont = [symbol] + target_cont
    source_cont = [c[:3] for c in source_cont]
    target_cont = [d[:3] for d in target_cont]
    matrix = copy.deepcopy(table)
    for i in range(len(source_cont)):
        row = matrix[i]
        row.insert(0, i)
        row.insert(1, source_cont[i])
    first_row = [' ', ' ']
    second_row = [' ', ' '] + target_cont
    for i in range(len(target_cont)):
        first_row.append(i)
    matrix.insert(0, first_row)
    matrix.insert(1, second_row)
    rows = len(matrix)
    cols = len(matrix[0])
    for row in range(rows):
        for col in range(cols):
            print('{0}'.format(matrix[row][col]).center(7), end='   ')
        print()

print("\nEdit Distance Table: ")
print_editdist = printing(source_cont, target_cont, score_matrix)

print("\nBacktrace Table: ")
print_traceback = printing(source_cont, target_cont, backtrace)

print("\nMaximum value in distance table: ", max_v)
print("\nMaxima: ")
indices = []
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        if matrix[i][j] == max_v:
            indices.append([i, j])
            print("    ", [i, j])

print("\nMaximal-similarity alignments:")
i = 0
for index in indices:
    seq1_aligned, seq2_aligned, xc, yc = back_trace(backtrace, (index[0], index[1]))
    edit_dist = edit_action(seq1_aligned, seq2_aligned)
    l = len(str(max(seq1_aligned + seq2_aligned, key=len)))
    edit_dist = ''.join(edit_dist)
    print("\t Alignment ", i, "( length ", len(seq1_aligned), "):")
    print("\t\tSource at\t\t{0}\t:".format(xc), end=' ')
    for str1 in seq1_aligned:
        print("{0}".format(str1).center(l+3), end=' ')
    print()
    print("\t\tTarget at\t\t{0}\t:".format(yc), end=' ')
    for str2 in seq2_aligned:
        print("{0}".format(str2).center(l+3), end=' ')
    print()
    print("\t\tEdit action\t\t\t:", end=' ')
    for str3 in edit_dist:
        print("{0}".format(str3).center(l+3), end=' ')
    print()
    i += 1
