# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 21:42:09 2017

@author: manoj
"""

import pickle
import pandas as pd
import nltk 
files = ["train.csv","test.csv"]

category_list = ["Atheism", "Climate Change is a Real Concern", 
                "Feminist Movement", "Hillary Clinton", "Legalization of Abortion"]
                
with open('MPQA_words.pkl', 'rb') as handle:
    words_with_value = pickle.load(handle)

for target in category_list:
    target_for_file  = target.replace(" ","_")  
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
        for i in words_with_value:
            f.write(i+",")
        f.write("label")
        f.write("\n")
        
        
        
        for i in range(0, len(all_tweets)):
            if category[i] == target:
                one_tweet = all_tweets[i]
                #one_tweet = all_tweets[i].lower()
                #one_tweet = re.sub(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)',"",one_tweet)
                text = nltk.word_tokenize(one_tweet)
                for j in words_with_value:
                    if j in text:
                        #f.write("1,")
                        f.write(str(words_with_value[j])+",")
                    else:
                        f.write("0,")
                f.write(stance[i])
                f.write("\n")
                        
        f.close()            
