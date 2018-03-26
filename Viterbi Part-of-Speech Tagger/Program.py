# Programming assigment 2 by Syed Abrar Ahmed
# For running the below program please run the below command preceded by the location where this file is located in command prompt or terminator.
# location of file > python NlpPA2.py <training_file_name> <test_file_name>

import sys
import collections
from collections import defaultdict

source_file = sys.argv[1] + ".txt"
source = open(source_file, "r")
source_cont = source.read()
print("\nUniversity of Central Florida\nCAP6640 Spring 2018 - Dr. Glinos")
print("\nViterbi Algorithm HMM Tagger by Syed Abrar Ahmed")

print("\n\nAll tags observed:\n")
def pos_tags():
    l = []
    with open(source_file, "r") as f:
        for line in f:
            try:
                l.append(line.split()[1])
            except:
                pass
        m = list(set(l))
        m = sorted(m)
    return m

pos = pos_tags()

def lemmatization(words):
    lemmatized_data = [''] * len(words)
    for index, word in enumerate(words):
        if word.endswith("sses") or word.endswith("xes") or word.endswith("ches") or word.endswith("shes"):
            new = word[:-2]
        elif word.endswith("ses") or word.endswith("zes"):
            new = word[:-1]
        elif word.endswith("men"):
            new = word[:-2] + "an"
        elif word.endswith("ies"):
            new = word[:-3] + "y"
        else:
            new = word
        lemmatized_data[index] = new
    return lemmatized_data


def print_alltags():
    for i, j in enumerate(pos, start=1):
        print(i, j)

print_alltags()

print("\nInitial Distribution:\n")
def calc_initial_dist():
    a = []
    myList = []

    for i in source_cont.rstrip("\n\n").split("\n\n"):
        a.append(i.split("\n"))

    count = 0
    prob = 0
    for tag in pos:
        for sentence in a:
            if tag == sentence[0].split(" ")[1]:
                count = count + 1
        prob = round((count/len(a)), 6)
        myList.append("%6f" %prob)
        count = 0

    return myList

prob_list = calc_initial_dist()

def print_initial_dist():
    for i in range(0, 44):
        if prob_list[i] != "0.000000":
            print("start [", pos[i], "| ]", prob_list[i])

print_initial_dist()

def create_words_tags_dict(pos_tags, just_words):
    words_tags_dict = {}
    for index in range(len(pos_tags)):
        words_tags_dict[just_words[index]] = words_tags_dict.get(just_words[index], {})
        words_tags_dict[just_words[index]][pos_tags[index]] = words_tags_dict[just_words[index]].get(pos_tags[index], 0)
        words_tags_dict[just_words[index]][pos_tags[index]] += 1
    return words_tags_dict

print("\nEmission Probabilities:\n")
def calc_emission_prob(words_tags_dict, pos_tags):
    emission_prob_dict = {}
    for word, tags_dict in sorted(words_tags_dict.items()):
        emission_prob_dict[word] = tags_dict
        for tag, count in tags_dict.items():
            tag_occur_in_text = pos_tags.count(tag)
            emission_prob = count / tag_occur_in_text
            emission_prob_dict[word][tag] = round(emission_prob, 6)
            print("\t\t{0}\t\t{1}\t\t{2:.6f}".format(word.center(25), tag.center(25), emission_prob))
    return emission_prob_dict

a = defaultdict(list)
for e, f in enumerate(source_cont.rstrip("\n\n").split("\n\n")):
    a[e] = f.split("\n")

main_list = []

for index, word in a.items():
    sub_list = [[], []]
    for i, j in enumerate(word):
        z = j.split(" ")
        sub_list[0].append(z[0])
        sub_list[1].append(z[1])
    main_list.insert(index, sub_list)
pos_tags = []
just_words = []
list_of_tags = []

for item in main_list:
    list_of_tags.append(item[1])
    pos_tags += item[1]
    just_words += item[0]
just_words = [word.lower() for word in just_words]
pieces = lemmatization(just_words)
words_tags_dict = create_words_tags_dict(pos_tags, pieces)
emission_prob_dict = calc_emission_prob(words_tags_dict, pos_tags)

def create_tag_tag(list_of_tags):
    tag_tag = {}
    start_tags = []
    end_tags = []
    for tag in list_of_tags:
        start_tags.append(tag[0])
        length = len(tag)
        end_tags.append(tag[length - 1])
        tag.insert(0, "START")
        tag.append("END")
        for i in range(len(tag) - 1):
            tag_tag[tag[i]] = tag_tag.get(tag[i], {})
            tag_tag[tag[i]][tag[i + 1]] = tag_tag[tag[i]].get(tag[i + 1], 0)
            tag_tag[tag[i]][tag[i + 1]] += 1
    return tag_tag

def calc_transition_prob(tag_tag):
    transition_prob_dict = {}
    for key, value in tag_tag.items():
        transition_prob_dict[key] = value
        total_count = sum(value.values())
        for inner_tags, value in value.items():
            transition_prob_dict[key][inner_tags] /= total_count
    return transition_prob_dict

tag_tag = create_tag_tag(list_of_tags)
transition_prob_dict = calc_transition_prob(tag_tag)

def print_transition_prob(transition_prob_dict):
    count = 0
    for key in transition_prob_dict:
        tag_dict = transition_prob_dict[key]
        count = count + len(tag_dict)
        print("[{0:.6f}]".format((sum(tag_dict.values()))), end=" ")
        for tag, value in sorted(tag_dict.items()):
            print("[{0}|{1}] {2:.6f}".format(tag, key, value), end=" ")
        print()
    return count

print("\nTransition Probabilities:\n")
bigram_count = print_transition_prob(transition_prob_dict)

print("\nCorpus Features:\n")
print("\tTotal # tags\t\t:", len(pos))
print("\tTotal # bigrams\t\t:", bigram_count)
print("\tTotal # lexicals\t:", len(emission_prob_dict))
print("\tTotal # sentences\t:", len(a))

test_file = sys.argv[2] + ".txt"
test_data = open(test_file, "r")
test_sent = test_data.read()
test_sent = [word.lower() for word in test_sent.split()]

print("\nTest Set Tokens Found in Corpus:\n")
print()
for word in test_sent:
    print("\t\t", word, "  :", end='\t')
    words_dic = emission_prob_dict.get(word)
    sort_items = sorted(words_dic.items())
    ord_words = collections.OrderedDict(sort_items)
    for tag, val in ord_words.items():
        format_value = float(format(val, '.6f'))
        print(tag, "(", format_value, ")", end='\t')
    print()
print()


print("\nIntermediate Results of Viterbi Algorithm:\n")
print()
final_tags = {}
viterbi = []
backpointer = []
first_viterbi = {}
first_backpointer = {}
first_word_tags = emission_prob_dict[test_sent[0]].keys()
for tag in first_word_tags:
    if tag == "START":
        continue
    sensor_model = emission_prob_dict[test_sent[0]][tag]
    init_distribution = transition_prob_dict["START"][tag]
    first_viterbi[tag] = init_distribution * sensor_model
    first_backpointer[tag] = None
total = sum(first_viterbi.values())
print("Iteration  1 : \t\t", test_sent[0], ":", end=' ')
sorted_items = sorted(first_viterbi.items())
ord_dict = collections.OrderedDict(sorted_items)
for tag, prob in ord_dict.items():
    value = prob / total
    first_viterbi[tag] = value
    format_value = float(format(value, '.6f'))
    print(tag, " (", format_value, ",", first_backpointer[tag], " )", end=' ')
print()
final_tags[test_sent[0]] = max(first_viterbi, key=first_viterbi.get)
viterbi.append(first_viterbi)
backpointer.append(first_backpointer)
for index, word in enumerate(test_sent[1:]):
    corpus_tags = emission_prob_dict[word]
    prev_word_tags = viterbi.pop()
    print("Iteration", index + 2, ":", "\t\t", word, ":", end=' ')
    max_dict = {}
    max_tag_dict = {}
    viterbi_dict = {}
    for tag in corpus_tags:
        best_max = 0
        best_prev_tag = None
        for prev_tag in prev_word_tags:
            prev_prob = prev_word_tags[prev_tag]
            transit_prob = transition_prob_dict[prev_tag].get(tag, 0.0001)
            emission_prob = emission_prob_dict[word][tag]
            current_prob = prev_prob * transit_prob * emission_prob
            if current_prob > best_max:
                best_max = current_prob
                best_prev_tag = prev_tag
        max_dict[tag] = best_max
        max_tag_dict[tag] = best_prev_tag
    total = sum(max_dict.values())
    sorted_items = sorted(max_dict.items())
    ord_items = collections.OrderedDict(sorted_items)
    for max_tag, max_prob in ord_items.items():
        value = max_prob / total
        viterbi_dict[max_tag] = value
        format_value = float(format(value, ".6f"))
        print(max_tag, "(", format_value, ",", max_tag_dict[max_tag], ")", end=' ')

    viterbi.append(viterbi_dict)
    print()
    final_tags[word] = max(viterbi_dict, key=viterbi_dict.get)

print("\nViterbi Tagger Output:\n")
for i in range(len(test_sent)):
    print("\t\t", "{0}".format(test_sent[i]).center(7), " ", end='')
    print("{0}".format(final_tags[test_sent[i]]).center(5))



















