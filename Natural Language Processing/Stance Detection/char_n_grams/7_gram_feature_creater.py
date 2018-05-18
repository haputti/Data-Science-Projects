# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 21:42:09 2017

@author: manoj
"""

import pickle
import pandas as pd
import re
import nltk 
files = ["train.csv","test.csv"]
n=7

category_list = ["Atheism", "Climate Change is a Real Concern", 
                "Feminist Movement", "Hillary Clinton", "Legalization of Abortion"]


for target in category_list:
    target_for_file  = target.replace(" ","_")
    
    with open('7grams_'+target_for_file+'.pkl', 'rb') as handle:
        all_features = pickle.load(handle)
    
    writer_files = []
    writer_files.append("train_"+target_for_file+".csv")
    writer_files.append("test_"+target_for_file+".csv")
    
    
    for ii in range(0,len(files)):
        filename = files[ii]
        writer_file = writer_files[ii]
        
        data       = pd.read_csv(filename)
        all_tweets = data["Tweet"]
        category   = data["Target"]
        stance     = data["Stance"]
        
        f = open(writer_file, 'w')
        for i in all_features:
            f.write(i+",")
        f.write("label")
        f.write("\n")
        
        
        
        for i in range(0, len(all_tweets)):
            if category[i] == target:
                one_tweet = all_tweets[i]
                one_tweet = all_tweets[i].lower()
                one_tweet = re.sub(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)',"",one_tweet)
                grams = [one_tweet[ii:ii+n] for ii in range(len(one_tweet)-n+1)]
                         
                for kk in range(0,len(grams)):
                    grams[kk] = grams[kk].replace(",","-")
                    
                for j in all_features:
                    if j in grams:
                        f.write("1,")
                    else:
                        f.write("0,")
                        
                f.write(stance[i])
                f.write("\n")
                        
        f.close()
    print(target+" done.")
