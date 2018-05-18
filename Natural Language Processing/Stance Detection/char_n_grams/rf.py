# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 19:06:09 2017

@author: manoj
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
targets = ["Atheism","Climate_Change_is_a_Real_Concern","Feminist_Movement",
           "Hillary_Clinton","Legalization_of_Abortion"]

#targets = ["Atheism"]           
#targets = ["Feminist_Movement"] 
          
for target in targets:
    class_variable = "label"
    if target == "Feminist_Movement":
        class_variable = "label.1"
        
    train_data = pd.read_csv("train_"+target+".csv")
    train_labels = train_data[class_variable]
    train_labels = list(train_labels)
    #Remove the label from train data frame
    del train_data[class_variable]
    
    test_data = pd.read_csv("test_"+target+".csv")
    test_labels = test_data[class_variable]
    test_labels = list(test_labels)
    #Remove the label from test data frame
    del test_data[class_variable]
    clf = RandomForestClassifier(max_depth=3, random_state=0 , n_estimators= 50)
    
    clf.fit(train_data, train_labels)
    model_answers = clf.predict(test_data)
    #actual_answers = data_frame[p_field].fillna("NAN")
    #print("Model Built")
    correct_count =0
    
            
    for ii in range(0,len(model_answers)):
        if model_answers[ii]==test_labels[ii]:
            correct_count +=1
                    
    accuracy = float(correct_count)/float(len(model_answers))*100 
    print("Accuracy for "+target+" is: "+str(round(accuracy,2)))
    