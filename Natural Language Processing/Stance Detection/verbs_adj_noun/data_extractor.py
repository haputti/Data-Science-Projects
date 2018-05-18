# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 18:29:16 2017

@author: manoj
"""
import pandas as pd
import re
import nltk 
import pickle
filename = "train.csv"
data       = pd.read_csv(filename)
all_tweets = data["Tweet"]   
category   = data["Target"]

category_list = ["Atheism", "Climate Change is a Real Concern", 
                "Feminist Movement", "Hillary Clinton", "Legalization of Abortion"]

              
for target in category_list:
    nouns = set()
    adjectives = set()
    verbs = set()
    for i in range(0, len(all_tweets)):
        if category[i] == target:
            one_tweet = all_tweets[i]
            #one_tweet = all_tweets[i].lower()
            #one_tweet = re.sub(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)',"",one_tweet)
            text = nltk.word_tokenize(one_tweet)
            a = nltk.pos_tag(text)
            for j in a:
                if j[1] == "NN" or j[1] == "NNS" or j[1]=="NNP" or j[1]=="NNPS":
                    nouns.add(j[0])
                if j[1] == "JJ" or j[1] =="JJR" or j[1] == "JJS":
                    adjectives.add(j[0])
                if j[1] == "VB" or j[1] =="VBD" or j[1] == "VBG" or j[1] == "VBN" or j[1] == "VBP" or j[1] == "VBZ":
                    verbs.add(j[0])
            print(str(i)+"-th tweet is: "+target)
     
   
    target_for_file  = target.replace(" ","_")
    with open('nouns_'+target_for_file+'.pkl', 'wb') as handle:
        pickle.dump(nouns, handle)
        
    with open('verbs_'+target_for_file+'.pkl', 'wb') as handle:
        pickle.dump(verbs, handle)  
    
    with open('adjectives_'+target_for_file+'.pkl', 'wb') as handle:
        pickle.dump(adjectives, handle)   
    
    