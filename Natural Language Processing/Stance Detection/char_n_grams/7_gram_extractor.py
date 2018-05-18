# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 18:29:16 2017

@author: manoj
"""
import pandas as pd
import re
import nltk 
import pickle

n=7
threshold = 10


filename = "train.csv"
data       = pd.read_csv(filename)
all_tweets = data["Tweet"]   
category   = data["Target"]

category_list = ["Atheism", "Climate Change is a Real Concern", 
                "Feminist Movement", "Hillary Clinton", "Legalization of Abortion"]

#category_list = ["Atheism"]    
          
for target in category_list:
    n_grams = {}
    for i in range(0, len(all_tweets)):
        if category[i] == target:
            one_tweet = all_tweets[i]
            one_tweet = all_tweets[i].lower()
            one_tweet = re.sub(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)',"",one_tweet)
            grams = [one_tweet[ii:ii+n] for ii in range(len(one_tweet)-n+1)]
            for all_7_grams in grams:
                all_7_grams = all_7_grams.replace(",","-")
                if all_7_grams in n_grams:
                    n_grams[all_7_grams] +=1
                else:
                    n_grams[all_7_grams] = 1      
            print(str(i)+"-th tweet is: "+target)
    

    char_7_grams_list = []
    for i in n_grams:
        if n_grams[i] >=threshold:
            char_7_grams_list.append(i)
   
    target_for_file  = target.replace(" ","_")
    
    with open('verbs_'+target_for_file+'.pkl', 'rb') as handle:
        verbs = pickle.load(handle)
    
    with open('nouns_'+target_for_file+'.pkl', 'rb') as handle:
        nouns = pickle.load(handle)
    
    with open('adjectives_'+target_for_file+'.pkl', 'rb') as handle:
        adjectives = pickle.load(handle) 
        
    nouns_list = list(nouns)
    verbs_list = list(verbs)
    adjectives_list = list(adjectives)
    
    nouns_verbs_adjectives =  nouns_list + verbs_list + adjectives_list
    nouns_verbs_adjectives = set(nouns_verbs_adjectives)
    nouns_verbs_adjectives = list(nouns_verbs_adjectives)
    
    """char_7_grams_list = []
    for i in n_grams:
        char_7_grams_list.append(i)"""
    
        
    all_features = nouns_verbs_adjectives + char_7_grams_list 
    all_features = set(all_features)
    all_features = list(all_features)
    
    all_features_lower = []
    for i in all_features:
        all_features_lower.append(i.lower())
     
    all_features_lower = set(all_features_lower)
    all_features_lower = list(all_features_lower)
    
    with open('7grams_'+target_for_file+'.pkl', 'wb') as handle:
        pickle.dump(all_features_lower, handle)
        
    
    