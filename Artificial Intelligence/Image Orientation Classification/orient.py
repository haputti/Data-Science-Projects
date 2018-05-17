import sys
import time
import numpy as np
from math import log
from collections import defaultdict, Counter
import random
import json

#Reading data
def read_data(fname):
    file = open(fname, 'r');
    data = [i.strip().split() for i in file.readlines()]
    image_names = [i[0] for i in data]
    exemplars = [map(int, i[1:]) for i in data]
    exemplars_array =[np.array(i) for i in exemplars]
    if (model == 'nearest'): 
        return image_names, exemplars_array
    else: 
        return image_names, exemplars
 
#-------------------------------K-Nearest Neighbours----------------------------------- 
def knn(trainfile, testfile, k, imagenames):
    count = 0
    f1 = open("output.txt", 'w');  
    for i in range(len(testfile)):
        #print "Time for test file", i, time.strftime("%X")
        orientation_list = []
        for j in range(len(trainfile)):
            orientation_list.append((trainfile[j][0],np.linalg.norm(testfile[i][1:] - trainfile[j][1:])))
        sorted_list = sorted(orientation_list, key=lambda x: x[1])
        orients = [j[0] for j in sorted_list[0:k]]
        orientation = Counter(orients).most_common()[0][0]
        f1.write(imagenames[i]+" "+str(orientation)+"\n")
        if (testfile[i][0] == orientation):
            count += 1  
    return (float(count)/float(len(testfile)))*100


#---------------------------------Ada Boost---------------------------------------------

#----Training------
#Creating the decision stumps
def create_pairs(K):
    decision_stumps = []
    for i in range(K):
        decision_stumps.append((random.randint(1, 192), random.randint(1, 192)))
    return decision_stumps

#Learning Algorithm
def stump(examples, indices, orientation_pair):
    greater = defaultdict(int)
    lesser = defaultdict(int)
    for image in examples:
        if image[indices[0]] >= image[indices[1]]:
            greater[image[0]] += 1
        else:
            lesser[image[0]] += 1
    if len(greater) == 0: return min(lesser, key = lesser.get), max(lesser, key = lesser.get)
    elif len(lesser) == 0: return max(greater, key = greater.get), min(greater, key = greater.get)
    else: return max(greater, key = greater.get), max(lesser, key = lesser.get)

#Ada boost Algorithm
def adaboost(examples, orientation_pair, K = 500):
    N = len(examples)
    pairs = create_pairs(K)
    W = [1.0/float(N) for i in range(N)]
    hypotheses, Z = [], []
    for k in range(0,K):
        indices = pairs[k]
        h = stump(examples, indices, orientation_pair)
        hypotheses.append(h)
        error = 0
        predictions = []
        for i in range(N):
            predictions.append(h[0] if examples[i][indices[0]] >= examples[i][indices[1]] else h[1])
        for i in range(N):
            if predictions[i] != examples[i][0]:
                error = error + W[i]
        for i in range(N):
            if predictions[i] == examples[i][0]:
                W[i] = W[i] * (error/(1 - error ))
        W = [float(w)/sum(W) for w in W]
        Z.append(log((1 - error )/error))
    return hypotheses, Z, pairs
    
#--------------------------------Neural Nets-----------------------------------------
def read_data_nnt(fname):
    train_data = []
    file = open(fname, 'r');
    for line in file:
        image_data = [w for w in line.split()]
        train_data.append(image_data)
    return train_data

def input_output(train_data):
    input_vector = []
    output_vector = []
    for image_vectors in train_data :
        input_vector.append(map(float,image_vectors[2:]))
        if image_vectors[1] == '0':
            output_vector.append([0.88,0.04,0.04,0.04])
        if image_vectors[1] == '90':
            output_vector.append([0.04,0.88,0.04,0.04])
        if image_vectors[1] == '180':
            output_vector.append([0.04,0.04,0.88,0.04])
        if image_vectors[1] == '270':
            output_vector.append([0.04,0.04,0.04,0.88])
    return input_vector,output_vector    

#sigmoid function
def sigmoid(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))


## Neural Network function
def nnt_train():
  X_train = np.array(train_input_vector)
  y_train = np.array(train_output_vector)
  global weight_0_1
  global weight_1_2
  weight_0_1 = np.random.uniform(-1,1,(192,20))
  weight_1_2 = np.random.uniform(-1,1,(20,4))
  np.random.seed(1)
  for iter in xrange(1000):
    # Forward Propagation
    layer_0 = X_train
    layer_1 = sigmoid(np.dot(layer_0,weight_0_1)) 
    layer_2 = sigmoid(np.dot(layer_1,weight_1_2)) 
    # From here backward propagation starts
    layer_2_error = y_train - layer_2
    layer_2_delta = layer_2_error * sigmoid(layer_2,deriv =True)

    layer_1_error = layer_2_delta.dot(weight_1_2.T)
    layer_1_delta = layer_1_error * sigmoid(layer_1,deriv=True)     
 
    weight_0_1 += np.dot(layer_0.T,layer_1_delta)*0.0001 
    weight_1_2 += np.dot(layer_1.T,layer_2_delta)*0.0001
    
  print layer_2
#--------end of Training---------

#Testing based on the trained model
def testing_adaboost(testfile, hypotheses, weights, indices, orientationpairs):
    results = []
    orientation_pairs = [(0,90),(90,180),(180,270),(0,270),(90,270),(0,180)]
    for p in orientationpairs:
        #print type(p)
        orient_dict = defaultdict(int)
        for j in range (0,100):
            if testfile[indices[p][j][0]] >= testfile[indices[p][j][1]]:
                orient_dict[hypotheses[p][j][0]] += weights[p][j] 
            else:
                orient_dict[hypotheses[p][j][1]] += weights[p][j]
        results.append(max(orient_dict, key = orient_dict.get))
    if Counter(results).most_common()[0][1] == Counter(results).most_common()[1][1]:
        return results[orientation_pairs.index((Counter(results).most_common()[0][0],Counter(results).most_common()[1][0]))]
    else:
        return Counter(results).most_common()[0][0]

def nnt_test(weight_0_1,weight_1_2): 
  # Testing starts    
  X_test = np.array(test_input_vector)
  global orientation_nnt
  orientation_nnt =[]

  l0 = X_test
  l1 = sigmoid(np.dot(l0,weight_0_1)) 
  l2 = sigmoid(np.dot(l1,weight_1_2))
  for x in l2:
      k = np.unravel_index(x.argmax(),x.shape)
      orientation_nnt.append(k[0]*90)
  #print "this is orientation \n", orientation_nnt
  count = 0
  for i in range(0,len(orientation_nnt)):
      if orientation_nnt[i] == int(test_image_vectors[i][1]):
       count += 1
  #print count
  print "Accuracy of Neural net:", (float(count)/len(orientation_nnt))*100
  
#--------------------------Main program----------------------------------

#if len(sys.argv) != 4:
#    print "Usage: python orient.py train train-data.txt model.txt nearest"
#    sys.exit()

action = str(sys.argv[1])
#action = "test"
model = str(sys.argv[4])
#model = "adaboost"


if action == 'train': 
    train_file = sys.argv[2]
 #   train_file = "train-data.txt"
    print "Training classifiers..."
    
    if(model=="nearest"):
        with open(train_file) as f:
            with open("nearest_model.txt", "w") as f1:
                for line in f: 
                    f1.write(line)
                    
    elif(model=="adaboost"):
        imagename, trainfile = read_data(train_file)
        splits = defaultdict(list)
        orientation_pairs = [(0,90),(90,180),(180,270),(0,270),(90,270),(0,180)]
        for image in trainfile:
            for pair in orientation_pairs:
                if image[0] in pair:
                    splits[pair].append(image)
        
        hypotheses = defaultdict(list)
        weights = defaultdict(list)
        indices = defaultdict(list)
          
        for p in orientation_pairs:
            h, z, i = adaboost(splits[p], p, 100)
            hypotheses[p] = h
            weights[p] = z
            indices[p] = i
            
        hypotheses = {str(k):v for k,v in hypotheses.items()}
        weights = {str(k):v for k,v in weights.items()}
        indices = {str(k):v for k,v in indices.items()}
        
        training_parameters = {"hypotheses": hypotheses, "weights": weights, "indices": indices}
        
        with open('adaboost_model.txt', 'w') as file:
             file.write(json.dumps(training_parameters))
           
    elif(model=="nnet" or model == 'best'):
        train_image_vectors = read_data_nnt(train_file)
        
        train_input_vector,train_output_vector = input_output(train_image_vectors)
        

        train_input_vector = np.array(train_input_vector)
        train_input_vector /= (255)
        
        # Calling the training function
        nnt_train()
        weight_0_1 = weight_0_1.tolist()
        weight_1_2 = weight_1_2.tolist()
        masterArray =[]
        
        # Writing the nnt_model file
        with open('nnet_model.txt','w') as f_w:
            masterArray.append(weight_0_1)
            masterArray.append(weight_1_2)
            json.dump(masterArray,f_w)
        with open('best_model.txt','w') as f_w:
            masterArray.append(weight_0_1)
            masterArray.append(weight_1_2)
            json.dump(masterArray,f_w)

    else:
        print "Invalid model name"

elif action == 'test': 
    test_file = sys.argv[2]
 #   test_file = "test-data.txt"
    model_file = sys.argv[3]
 #   model_file = "adaboost_model.txt"
    print "Testing classifiers..."
    if(model=="nearest"):
        testimage_names, testfile = read_data(test_file)
        trainimage_names, trainfile = read_data(model_file)
        print "Accuracy of KNN is :", knn(trainfile, testfile, 11, testimage_names),"%"
                    
    elif(model=="adaboost"):
        testimage_names, testfile = read_data(test_file)
        f2 = open("adaboost_output.txt", 'w');      
        with open(model_file, 'r') as f:
            datastore = json.load(f)
            
        hypotheses = datastore['hypotheses']
        weights = datastore['weights']
        indices = datastore['indices']
                     
        print "Testing..."
        
        count = 0
        for i in testfile:
            orientationpairs = ['(0, 90)','(90, 180)','(180, 270)','(0, 270)','(90, 270)','(0, 180)']
            orientation = testing_adaboost(i, hypotheses, weights, indices, orientationpairs)
            f2.write(testimage_names[testfile.index(i)]+" "+str(orientation)+"\n")            
            if i[0] == orientation:
                count += 1
        print "Accuracy of Adaboost is:", (float(count)/float(len(testfile)))*100

        
    elif(model=="nnet" or model == 'best'):
        test_image_vectors = read_data_nnt(test_file)
        test_input_vector, test_output_vector = input_output(test_image_vectors)
        test_input_vector = np.array(test_input_vector)
        test_input_vector /= 255
        with open(model_file,'r') as f :
            arrays = json.load(f)
            w0 = np.asarray(arrays[0])
            w1 = np.asarray(arrays[1])
        nnt_test(w0,w1)
        with open("output.txt", 'w') as output_file :
            for i in range(0,len(test_image_vectors)):
                output_file.write(test_image_vectors[i][0]+' '+str(orientation_nnt[i])+"\n")
   
    else:
        print "Invalid model name"
        
        
else: print "Invalid input"
