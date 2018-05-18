# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 18:29:16 2017

@author: manoj
"""
import pandas as pd
import nltk 
import pickle
filename = "subjclueslen1-HLTEMNLP05.tff"

data= []
words_with_value = {}
with open(filename) as f:
    for line in f:
        line = line.split("\n")[0]
        line = line.split("\r")[0]
        fields = line.split(" ")
        if len(fields) == 7:
            fields.pop(5)
        word  = fields[2].split("=")[1]
        word_type = fields[0].split("=")[1]
        polarity  = fields[5].split("=")[1]
        
        if(polarity == "positive"):
            if(word_type == "strongsubj"):
                words_with_value[word] = 2
            else:
                #Its a positive weak word
                words_with_value[word] = 1

        elif(polarity == "negative"):
            if(word_type == "strongsubj"):
                words_with_value[word] = -2
            else:
                #Its a negative weak word
                words_with_value[word] = -1
        else:
            words_with_value[word] = 0
            

with open('MPQA_words.pkl', 'wb') as handle:
        pickle.dump(words_with_value, handle)
    
    