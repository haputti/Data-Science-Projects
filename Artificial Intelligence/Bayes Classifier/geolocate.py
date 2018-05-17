'''
#!/usr/bin/python
# Tweet Classificattion Based on Bayes law:

# Bayes Theorem -
                P(Y/X) = P(X/Y) * P(Y) / P(X)
                we need to evaluate Posterior probabilities, P(Y-cities y1,y2,y3.../X-Words w1,w2,w3...)
                P(X) - Constant So will Not Calculate P(X)

# Accuracy Of our Bayesian Model is 46.4%
# The Top 5 Words Associated with each 12 cities are are display on the screen.
# The Results can be found in output folder.

#Refernces:
1) https://en.wikipedia.org/wiki/Naive_Bayes_classifier
2) https://www.youtube.com/watch?v=psHrcSacU9Y
3)https://machinelearningmastery.com/naive-bayes-classifier-scratch-python/
4) Canvas and lecture videos
'''

import re
import numpy as np
import sys

cities = ['Chicago,_IL', 'Boston,_MA', 'San_Francisco,_CA', 'Toronto,_Ontario', 'San_Diego,_CA', 'Atlanta,_GA', 'Manhattan,_NY', 'Washington,_DC', 'Houston,_TX', 'Philadelphia,_PA', 'Los_Angeles,_CA', 'Orlando,_FL']
city_mapping = {}
cIndex = 0

for city in cities:
    city_mapping[city] = cIndex
    cIndex += 1

# Reading Each tweet and split in words
lineList = []
i = 0
def read_data(file_name):
    data = {}
    n = 0
    with open(file_name, 'r') as f:
        for line1 in f:
            line1 = line1
            n += 1
            y, x = line1.split(',', 1)
            words = x.split(" ")
            y = y + "," + words[0]
            x = x.lower().strip()
            x = re.sub('[^A-Za-z ]', '', x)
            x = re.sub(' +', ' ', x)

            words = x.split(" ")
            words = words[1:]

            w1 = {}
            for word in words:
                if word in ['','a','an','the']:
                    continue
                w1[word] = 1

            temp = data.get(city_mapping[y], [])
            temp.append(w1)
            data[city_mapping[y]] = temp

    return data,n


train_data,n_train = read_data(sys.argv[1])
test_data,n_test = read_data(sys.argv[2])

y_probs = []
#print train_data


#Calcutating P(Y) for Each Cities,tweet pairs
city_prob = {}
for w in cities:
    city_prob[city_mapping[w]]=float(len(train_data[city_mapping[w]]))/n_train
    #city_prob[w]=(float(len(train_data[w]))/n)
#print city_prob


# Calculating P(X|Y)
probs = {}
cap = 0
#print(len(train_data[0]))
for i in range(len(city_prob.keys())):
    for tweet in train_data[i]:
        for k,v in tweet.items():
            probs[k] = probs.get(k,[0 for j in range(len(city_prob.keys()))])
            probs[k][i] += 1./len(train_data[i])

# Test data
#print("Number of test examples: ",n_test)
#X_test = np.array([item for k,v in test_data.items() for item in v])
#print(len(X_test))

#Implementing model into Test Data :
test_probs = np.ones((n_test,len(city_prob.keys())))
tIndex = 0
y_test = []
for testClass,tweetList in test_data.items():
    for tweet in tweetList:
        y_test.append(testClass)
        for classIndex in range(len(city_prob.keys())):
            for word in tweet:
                temp = probs.get(word,None)
                if not temp:
                    continue
                else:
                    test_probs[tIndex][classIndex] *= temp[classIndex]/city_prob[classIndex]
        tIndex+=1

y_preds = np.argmax(test_probs,axis=1)
#print(len(y_test))
#print(len(y_preds))

#Calculating Accuracy
TP = sum([y_preds[i]==y_test[i] for i in range(len(y_preds))])
accuracy=(float(TP)/len(y_preds))*100
#print "Accuracy :" + str(accuracy)+"%"

#creating the  the output file
with open(sys.argv[3],'w') as file:
    file.write(str(accuracy))

# Writing output
with open("output.txt",'w') as outFile:
    with open(sys.argv[2],'r') as inFile:
        i = 0
        for line in inFile:
            outText =  str(cities[y_preds[i]]) + " " +line
            outFile.write(outText)
            i+=1
outFile.close()
inFile.close()


#printing Top 5 Words for Each Cities
words = probs.keys()
top5 = {}
for i in range(len(city_prob.keys())):
    probByClass = []
    for k,v in probs.items():
        probByClass.append(v[i])
    sortedIndices = sorted(range(len(probByClass)),key=lambda x:probByClass[x])
    sortedIndices = sortedIndices[::-1]
    top5[cities[i]] = [words[j] for j in sortedIndices[:5]]
print(top5)
