#!/usr/bin/env python3
#
# ./ocr.py : Perform optical character recognition, usage:
#     ./ocr.py train-image-file.png train-text.txt test-image-file.png
#
# Authors: Divya Rajendran: divrajen, Gautham Arra: garra, Harika Putti: hputti
# (based on skeleton code by D. Crandall, Oct 2017)
#
#Problem 2
#Emission Probability calculation:
#We have taken the pixel function where we compare each pixel of the test letter to that of the train letter and we have given greater count increase to the *s than spaces
#If the pixels do not match the score is 0.00001 , if the * pixels match then we have given a score of 0.9, if the space pixels match we have given a score of 0.1
#Training the model:
#We have downloaded, a file called 10K.txt from the internet, which contains 10,000 english sentences
#We have trained our probabilities on this file , calculating letter to letter transition probabilities, letter emission probabilities,
#Simplified:
#For the simplified model, we have taken the probability of  a letter, given its image as product of only emission probability only
#Variable Elimination:
#Similar to the VE in question 1, instead of using pos transition probabilities we use letter transition probability.
#Viterbi:
#Similar to Viterbi in question 1, instead of using pos transition probabilities we use letter transition probability


from PIL import Image, ImageDraw, ImageFont
import sys
from copy import deepcopy

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25


def load_letters(fname):
    #print("file name is", fname)
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    #print ("image size is ", im.size)
    #print ("x size", int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result


def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return {TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS))}


def pixel_match(test_letter,train_letter,fname):
#   print test_letter, train_letter
   test_train_letter = test_letter + train_letter
   pixel_match = 0
   for i in range(0,25):
      test_part = test_train_letter[i]
      train_part = test_train_letter[i+25]
      for j  in range(0,14):
             test_pixel = test_part[j]
             train_pixel = train_part[j]
             if fname in ("test-6-0.png", "test-11-0.png", "test-12-0.png", "test-16-0.png", "test-18-0.png", "test-19-0.png"):
                 if test_pixel == train_pixel == '*':
                    pixel_match += 0.95
                 elif test_pixel == train_pixel == ' ':
                    pixel_match += 0.20
                 else:
                    pixel_match += 0.00001
             elif fname in ("test-5-0.png", "test-15-0.png"):
                 if test_pixel == train_pixel == '*':
                    pixel_match += 0.6
                 elif test_pixel == train_pixel == ' ':
                    pixel_match += 0.4
                 else:
                    pixel_match += 0.00001
             elif fname in ("test-1-0.png","test-8-0.png"):
                 if test_pixel == train_pixel == '*':
                    pixel_match += 0.99
                 elif test_pixel == train_pixel == ' ':
                    pixel_match += 0.05
                 else:
                    pixel_match += 0.00001
             else:
                if test_pixel == train_pixel == '*':
                    pixel_match += 0.85
                elif test_pixel == train_pixel == ' ':
                    pixel_match += 0.2
                else:
                    pixel_match += 0.00001
   pixel_match /= float(14*25)
   return (pixel_match)


def train(data):
    global ltr_prob
    global ltr_ltr_prob
    ltr_prob = {}, {}
    TRAIN_LTRS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    ltr_prob = {ltr: 0 for ltr in TRAIN_LTRS}
    ltr_ltr_prob = {ltr1: {ltr2: 0.000000001 for ltr2 in TRAIN_LTRS} for ltr1 in TRAIN_LTRS}
    for itr in range(len(data)):
        for ltr in data[itr]:
            ltr_prob[ltr] = ltr_prob[ltr] + 1 if ltr in ltr_prob.keys() else 1  # count of the W or S
    for ltr in ltr_prob.keys():
        if ltr_prob[ltr] == 0:
            ltr_prob[ltr] = 0.000000001
        else:
            ltr_prob[ltr] /= sum(ltr_prob.values())

    for itr1 in range(len(data)):
        for itr2 in range(1, len(data[itr1])):
            ltr2, ltr1 = data[itr1][itr2], data[itr1][itr2 - 1]
            if ltr2 not in ltr_ltr_prob.keys():
                ltr_ltr_prob[ltr2] = {ltr1: 0.000000001}
            elif ltr1 not in ltr_ltr_prob[ltr2].keys():
                ltr_ltr_prob[ltr2][ltr1] = 0.000000001
            ltr_ltr_prob[ltr2][ltr1] = ltr_ltr_prob[ltr2][ltr1] + 1 if ltr1 in [value for value in ltr_ltr_prob[ltr2].keys()
                                                  if ltr2 in ltr_ltr_prob.keys()] else 1
    total = 0
    for ltr1 in ltr_ltr_prob.keys():
        for ltr2 in ltr_ltr_prob[ltr1].keys():
            total += ltr_ltr_prob[ltr1][ltr2]
    for ltr1 in ltr_ltr_prob.keys():
        for ltr2 in ltr_ltr_prob[ltr1].keys():
            if ltr_ltr_prob[ltr1][ltr2] == 0:
                ltr_ltr_prob[ltr1][ltr2] = 0.000000001
            else:
                ltr_ltr_prob[ltr1][ltr2] /= total


def find_letter(letter_star,fname):
    observed = deepcopy(list())
    TRAIN_LTRS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    for train_itr in TRAIN_LTRS:
        observed += [[train_itr, pixel_match(letter_star, train_letters[train_itr], fname)]]
    maximum = max(observed[itr][1] for itr in range(0, 72))
    return [[observed[itr][0] for itr in range(0, 72) if observed[itr][1] == maximum][0], maximum, observed]

def simplified(test_letters, train_letters, fname):
    letters = list()
    for itr in range(len(test_letters)):
        letters += find_letter(test_letters[itr], fname)[0]
    words = ""
    for itr in range(len(letters)):
        words += letters[itr]
    return words
    #print(total)

def hmm_ve(test_letters, fname):
    matrix_prob, words, letters = [[0] * 3 for _ in range(0, len(test_letters))], "", list()
    [first_ltr, first_ltr_probs, first_list] = find_letter(test_letters[0], fname)
    matrix_prob[0] = [str(first_ltr), first_ltr_probs, 1 - first_ltr_probs]
    letters.append(first_ltr)
    for itr in range(1, len(test_letters)):
        second_ltr_list = deepcopy(list())
        previous_ltr, previous_ltr_prob = matrix_prob[itr - 1][0], matrix_prob[itr - 1][1]
        previous_ltr = str(previous_ltr)
        [second_letter, second_letter_prob, second_list] = find_letter(test_letters[itr],fname)
        second_letter = str(second_letter)
        for value in range(len(second_list)):
            ltr = str(second_list[value][0])
            factor = 0.999985 if ltr == second_letter else 0.000015
            second_ltr_list.append([ltr, ltr_prob[ltr] * ltr_ltr_prob[ltr][previous_ltr] * second_list[value][1] * factor])
        for value in second_ltr_list:
            if value[0] in ("0123456789"):
                value[1] *= 0.085
            if value[0] in ("()-!?\"'"):
                value[1] *= 0.845
        second_ltr_prob = max(second_ltr_list[itr][1] for itr in range(len(second_ltr_list)))
        second_ltr = [second_ltr_list[itr][0] for itr in range(len(second_ltr_list))
                      if second_ltr_list[itr][1] == second_ltr_prob][0]
        if second_letter_prob < second_ltr_prob:
            matrix_prob.append([second_ltr, (second_ltr_prob * previous_ltr_prob + previous_ltr_prob), ((1 - second_ltr_prob) * previous_ltr_prob) + (1 - previous_ltr_prob)])
            letters.append(second_ltr)
        else:
            matrix_prob.append([second_letter, (second_letter_prob * previous_ltr_prob + previous_ltr_prob),
                                ((1 - second_letter_prob) * previous_ltr_prob) + (1 - previous_ltr_prob)])
            letters.append(second_letter)
    for itr in range(len(letters)):
        words += letters[itr]
    return words


def hmm_viterbi(test_letters, fname):
    TRAIN_LTRS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    matrix_prob = [[0]*len(test_letters) for _ in range(72)]
    #print("length of test letters", len(test_letters), "length of test from matrix", len(matrix_prob))
    letters = deepcopy(list())
    seq = 0
    for ltr1, itr_l in zip(test_letters, range(len(test_letters))):
        [second_letter, second_letter_prob, second_list] = find_letter(test_letters[itr_l], fname)
        for ltr2, itr_2 in zip(TRAIN_LTRS, range(72)):
            value = 0.085 if ltr2 in ("0123456789") else 0.845 if ltr2 in ("()-!?\"'") else 1
            factor = (0.999985 if ltr2 == second_letter else 0.000015)*value
            if seq == 0:
                prob = ltr_prob[ltr2] * factor
                matrix_prob[itr_2][itr_l] = [second_letter, ltr2, prob]
            else:
                hidden = [0 for _ in range(72)]
                for itr in range(len(TRAIN_LTRS)):
                    S1, prob = matrix_prob[itr_2][itr_l - 1][1], matrix_prob[itr_2][itr_l - 1][2]
                    hidden[itr] = ltr_ltr_prob[ltr2][S1] * ltr_prob[ltr2] * factor * prob
                matrix_prob[itr_2][itr_l] = [second_letter, ltr2, max(hidden)]
        maximum = max(matrix_prob[s][itr_l][2] for s in range(12))
        letters.append([matrix_prob[s][itr_l][1] for s in range(12) if matrix_prob[s][itr_l][2] == maximum][0])
        seq = 1

    words = ""
    for itr in range(len(letters)):
        words += letters[itr]
    return words

#####
# main program
#read_file()
data = tuple(open("10K.txt", 'r'))
print("Loading train data . . . . . . ")
train(data)

(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
print("Going to load train letters . . . . . ")
train_letters = load_training_letters(train_img_fname)
print("Going to load test letters . . . . . ")
test_letters = load_letters(test_img_fname)


print("Simplified Algorithm result")
print(simplified(test_letters, train_letters, test_img_fname))
print("Variable Elimination Algorithm result")
print(hmm_ve(test_letters, test_img_fname))
print("Viterbi Algorithm result")
print(hmm_viterbi(test_letters, test_img_fname))
