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
    all_words = set()
    for i in range(0, len(all_tweets)):
        if category[i] == target:
            one_tweet = all_tweets[i]
            #one_tweet = all_tweets[i].lower()
            #one_tweet = re.sub(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)',"",one_tweet)
            text = nltk.word_tokenize(one_tweet)
            for j in text:
                j = j.replace(",","__")
                all_words.add(j)
            print(str(i)+"-th tweet is: "+target)
     
   
    target_for_file  = target.replace(" ","_")
    with open(target_for_file+'_all_words.pkl', 'wb') as handle:
        pickle.dump(all_words, handle)

    