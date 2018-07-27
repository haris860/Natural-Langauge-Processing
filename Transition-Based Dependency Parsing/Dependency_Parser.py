# Programming assigment 3 by Syed Abrar Ahmed
# For running the below program please run the below command preceded by the location where this file is located in command prompt or terminator.
# location of file > python NlpPA3.py <Corpus_file_name> <test_file_name>

import sys

source_file = sys.argv[1] + ".txt"
source = open(source_file, "r")
source_cont = source.read()
print("\nUniversity of Central Florida\nCAP6640 Spring 2018 - Dr. Glinos")
print("Dependency Parser by Syed Abrar Ahmed")

def pos_tags():
    l = []
    with open(source_file, "r") as f:
        for line in f:
            try:
                l.append(line.split()[2])
            except:
                pass
        m = list(set(l))
        m = sorted(m)
    return m

def tokens():
    l = []
    with open(source_file, "r") as f:
        for line in f:
            try:
                l.append(line.split()[1])
            except:
                pass
    return l

def print_Corpus_Stats():
    print("\nCorpus Statistics:")

    first_indexl = []
    operation1l = []
    first_wordl = []
    operation2l = []
    first_tagl = []
    first_valuel = []
    for line in source_cont.split("\n"):
        before, sep, after = line.partition(" ")
        first_indexl.append(before)
        operation1l.append(after)

    for line in operation1l:
        before, sep, after = line.partition(" ")
        first_wordl.append(before)
        operation2l.append(after)

    for line in operation2l:
        before, sep, after = line.partition(" ")
        first_tagl.append(before)
        first_valuel.append(after)

    new_sent = []
    main_sent = []

    for i in range(0, len(first_wordl)):
        if first_wordl[i] == "":
            main_sent.append(new_sent)
            new_sent = []
        elif first_wordl[i] != "":
            new_sent.append(first_indexl[i] + " " + first_wordl[i] + " " + first_tagl[i] + " " + first_valuel[i])

    sec_indexl = []
    sec_wordl = []
    sec_tagl = []
    sec_valuel = []
    for i in range(len(first_wordl)):
        if first_wordl[i] != "":
            sec_indexl.append(int(first_indexl[i]))
            sec_wordl.append(first_wordl[i])
            sec_tagl.append(first_tagl[i])
            sec_valuel.append(int(first_valuel[i]))

    thir_index = []
    thir_wordl = []
    thir_tagl = []
    thir_valuel = []
    for i in range(len(first_wordl)):
        if first_wordl[i] == "":
            thir_index.append(0)
            thir_wordl.append(0)
            thir_tagl.append(0)
            thir_valuel.append(0)
        else:
            thir_index.append(int(first_indexl[i]))
            thir_wordl.append(first_wordl[i])
            thir_tagl.append(first_tagl[i])
            thir_valuel.append(int(first_valuel[i]))

    dist_tags = set(sec_tagl)
    d_tags = []
    for i in dist_tags:
        d_tags.append(i)

    root_arcs = 0

    for i in range(len(sec_valuel)):
        if sec_valuel[i] == 0:
            root_arcs += 1

    larc_count = 0
    rarc_count = 0

    for i in range(len(sec_valuel)):
        if sec_valuel[i] > sec_indexl[i] and sec_valuel[i] != 0:
            larc_count = larc_count + 1
        elif sec_valuel[i] < sec_indexl[i] and sec_valuel[i] != 0:
            rarc_count = rarc_count + 1

    pos = pos_tags()
    toks = tokens()

    a = []
    for i in source_cont.rstrip("\n\n").split("\n\n"):
        a.append(i.split("\n"))

    print("\n\t# sentences  : ", len(a))
    print("\t# tokens     : ", len(toks))
    print("\t# POS tags   : ", len(pos))
    print("\t# Left-Arcs  : ", larc_count)
    print("\t# Right-Arcs : ", rarc_count)
    print("\t# Root-Arcs  : ", root_arcs)
    return first_wordl, first_indexl, first_tagl, first_valuel

word_l, index_l, tag_l, value_l = print_Corpus_Stats()

def print_left_arc_array():
    print("\n\nLeft Arc Array Nonzero Counts:")
    first_dict = {}
    first_numl = []
    sec_numl = []
    thir_numl = []
    frth_numl = []
    first_linel = []
    sec_linel = []
    thir_linel = []
    frth_linel = []
    h = 0
    b = ""
    first_str = ""
    n = 0
    for i in range(len(word_l)):
        if not word_l[i] == "":
            first_numl.append(int(index_l[i]))
            sec_numl.append(word_l[i])
            thir_numl.append(tag_l[i])
            frth_numl.append(int(value_l[i]))
        elif word_l[i] == "":
            for j in range(len(first_numl)):
                if frth_numl[j] > first_numl[j] and frth_numl[j] != 0:
                    h = frth_numl[j]
                    b = thir_numl[h-1]
                    first_str = thir_numl[j] + " " + b
                    if first_str not in first_dict:
                        first_dict[first_str] = 1
                        first_linel.append(thir_numl[j])
                        sec_linel.append(b)
                    elif first_str in first_dict:
                        n = first_dict.get(first_str)
                        n = n + 1
                        first_dict[first_str] = int(n)
            first_numl = []
            sec_numl = []
            thir_numl = []
            frth_numl = []

    left_array = []
    for d in first_dict:
        thir_linel.append(first_dict[d])

    for i in range(len(first_linel)):
        frth_linel.append([first_linel[i], sec_linel[i], thir_linel[i]])

    left_array = sorted(frth_linel)

    for i in range(len(left_array)):
        if left_array[i][0] == left_array[i - 1][0]:
            print("[  " + left_array[i][1] + ",  " + str(left_array[i][2]) + "] ", end="")
        else:
            print("")
            print(left_array[i][0] + " : [  " + left_array[i][1] + ",  " + str(left_array[i][2]) + "] ", end="")

    return left_array, first_dict

left_array, first_dict = print_left_arc_array()

def print_right_arc_array():
    print("\n\nRight Arc Array Nonzero Counts:")
    sec_dict = {}
    first_numl = []
    sec_numl = []
    thir_numl = []
    frth_numl = []
    fif_linel = []
    six_linel = []
    sev_linel = []
    eig_linel = []
    right_array = []
    for i in range(len(word_l)):
        if not word_l[i] == "":
            first_numl.append(int(index_l[i]))
            sec_numl.append(word_l[i])
            thir_numl.append(tag_l[i])
            frth_numl.append(int(value_l[i]))
        elif word_l[i] == "":
            for j in range(len(first_numl)):
                if frth_numl[j]<first_numl[j] and frth_numl[j] != 0:
                    h = frth_numl[j]
                    b = thir_numl[h-1]
                    first_str = thir_numl[j] + " " + b
                    if first_str not in sec_dict:
                        sec_dict[first_str] = 1
                        fif_linel.append(thir_numl[j])
                        six_linel.append(b)
                    elif first_str in sec_dict:
                        n = sec_dict.get(first_str)
                        n = n + 1
                        sec_dict[first_str] = int(n)
            first_numl = []
            sec_numl = []
            thir_numl = []
            frth_numl = []

    for w in sec_dict:
        sev_linel.append(sec_dict[w])

    for i in range(len(fif_linel)):
        eig_linel.append([fif_linel[i], six_linel[i], sev_linel[i]])

    rights_array = sorted(eig_linel)

    for i in range(len(rights_array)):
        if rights_array[i][0] == rights_array[i-1][0]:
            print("[  " + rights_array[i][1]+",  " + str(rights_array[i][2])+"] ", end="")
        else:
            print("")
            print(rights_array[i][0] + " : [  " + rights_array[i][1] + ",  " + str(rights_array[i][2]) + "] ", end="")

    return right_array, sec_dict


right_array, sec_dict = print_right_arc_array()

def print_arc_conf_array():
    sec_str = ""
    l = 0
    c = 0
    print("\n\nArc Confusion Array:")
    for i in range(len(left_array)):
        sec_str = left_array[i][0]+" " + left_array[i][1]
        if left_array[i][0] != left_array[i - 1][0]:
            print("")
            print(left_array[i][0] + " :", end="")
        if sec_str in sec_dict:
                l = sec_dict.get(sec_str)
                c += 1
                print("[ " + left_array[i][1]+", "+str(left_array[i][2])+", "+str(l)+"] ", end="")

    print("\n\n\tNumber of confusing arcs = "+str(c))
    print("")

print_arc_conf_array()

def print_stack_buff():
    input = []
    first_strl = []
    first_coll = []
    second_coll = []
    sec_strl = []
    fir_str = ""
    ctr1 = 0
    ctr2 = 0
    f1 = 0
    f2 = 0
    f3 = 0
    f4 = 0
    f5 = 0
    test_file = sys.argv[2] + ".txt"
    test_data = open(test_file, "r")
    test_sent = test_data.read()

    print("Input Sentence:")
    print(test_sent)
    print("")
    print("Parsing Actions and Transitions:")
    print("")

    test_sent = test_sent.strip()
    for line in test_sent.split("\n"):
        input.append(line)
    for line in test_sent.split("\n"):
        before, sep, after = line.partition("/")
        first_coll.append(before)
        second_coll.append(after)

    while f1 == 0:
        f2 = 0
        f3 = 0
        if len(first_strl) < 2 and len(input) != 0:
            print(first_strl, end="")
            print(input, end="")
            print(" SHIFT")
            first_strl.append(input[0])
            sec_strl.append(second_coll[0])
            del(input[0])
            del(second_coll[0])
            f2 = 1
            f5 = 1
        elif len(first_strl) >= 2:
            f3 = 0
            fir_str = sec_strl[-2] + " " + sec_strl[-1]
            if (sec_strl[-1][0] == "." or sec_strl[-1][0] == "R") and sec_strl[-2][0] == "V":
                print(first_strl, end="")
                print(input, end="")
                print("Right-Arc: "+first_strl[-2]+" --> "+first_strl[-1])
                del(first_strl[-1])
                del(sec_strl[-1])
                f2 = 1

            elif sec_strl[-2][0] == "I" and sec_strl[-1][0] == ".":
                print(first_strl, end="")
                print(input, end="")
                print(" SWAP")
                input.append(first_strl[-2])
                second_coll.append(sec_strl[-2])
                del(first_strl[-2])
                del(sec_strl[-2])
                f2 = 1

            elif (sec_strl[-2][0] == "V" or sec_strl[-2][0] == "I") and (sec_strl[-1][0] == "D" or sec_strl[-1][0] == "I" or sec_strl[-1][0] == "J" or sec_strl[-1][0] == "P" or sec_strl[-1][0] == "R") and (len(input) != 0):
                print(first_strl, end="")
                print(input, end="")
                print(" SHIFT")
                first_strl.append(input[0])
                sec_strl.append(second_coll[0])
                del (input[0])
                del (second_coll[0])
                f2 = 1

            elif (fir_str in first_dict) and (fir_str in sec_dict):
                ctr1 = first_dict.get(fir_str)
                ctr2 = sec_dict.get(fir_str)
                ctr1 = int(ctr1)
                ctr2 = int(ctr2)
                if ctr1 > ctr2:
                    print(first_strl, end="")
                    print(input, end="")
                    print(" Left-Arc: " + first_strl[-2] + " <-- " + first_strl[-1])
                    del(sec_strl[-2])
                    del(first_strl[-2])
                    f2 = 1
                    f3 = 1

                elif ctr2 > ctr1:
                    print(first_strl, end="")
                    print(input, end="")
                    print("Right-Arc: " + first_strl[-2] + " --> " + first_strl[-1])
                    del (first_strl[-1])
                    del (sec_strl[-1])
                    f2 = 1
                    f3 = 1

            elif fir_str in first_dict and f3 == 0:
                print(first_strl, end="")
                print(input, end="")
                print(" Left-Arc: " + first_strl[-2] + " <-- " + first_strl[-1])
                del (sec_strl[-2])
                del (first_strl[-2])
                f2 = 1

            elif fir_str in sec_dict and f3 == 0:
                print(first_strl, end="")
                print(input, end="")
                print("Right-Arc: " + first_strl[-2] + " --> " + first_strl[-1])
                del (first_strl[-1])
                del (sec_strl[-1])
                f2 = 1

        elif len(input) == 0:
                f5 = 1
                if len(first_strl) == 1:
                    print(first_strl, end="")
                    print(input, end="")
                    print(" ROOT -- > " + first_strl[0])
                    f1 = 1
                f2 = 1

        elif f2 == 0 and f5 == 0 and len(input) != 0:
            print(first_strl, end="")
            print(input, end="")
            print(" SHIFT")
            first_strl.append(input[0])
            sec_strl.append(second_coll[0])
            del (input[0])
            del (second_coll[0])

print_stack_buff()















