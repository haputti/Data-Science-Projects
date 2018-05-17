###################################
# CS B551 Fall 2017, Assignment #3
#
# Your names and user ids:
# Goutham Arra - garra   
# Harika Putti - haputti
# Divya Rajendran - divrajen
# (Based on skeleton code by D. Crandall)
#
#
####
# We have trained our model on bc.train file given to us. Accordingly, we have calculated the probability of a given part of speech, probability of word given pos, the probability of pos given another pos, and probability of pos starting a sentence(emission probability used in the VE and Viterbi ), and we have stored all the values in dictionary
#Simplified:
#Next we have defined our simplified model based on the figure 1b given in the question, where the probability of a pos given word is product of probability of word given pos and product of pos, and we have taken maximum of these products to select the best pos for a given word in a sentence
#Variable Elimination:
#For VE, we have implemented both forward and backward elimination of the variables to find the most probable pos at a given position in a sentence
#For forward elimination, we have created Tow table dictionary storing the residue probability at a given location by eliminating the variables to the left of it 
#Similarly, we have created Nu table dictionary storing the residue probability at a given location by eliminating the variables to the right of it 
#To find the most probable letter at any given location, we have multiplied the Tow and Nu at a given location that we want to find the found the maximum over 12 pos and selected the pos with the most probability
#Viterbi:
#For Viterbi, we have similarly, created Tow table at each location, which is the product of emission probability and transition probability(except for the first word) and Tow value from previous location. We take the max of Tow value at each location
#After calculating the Tow table, for the last location, we find the max prob. Pos , and from here we back track ,finding for what pos, we have gotten the maximum for the succeeding word.
#By this manner, we find the most probable pos sequence 

####

import random
import math


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    def posterior(self, sentence, label):
        x  = -(math.log(self.P_state[label[0]]))  
        for i in range(0,len(sentence)):
              word = sentence[i]
              state = label[i]
              if word in self.P_word_state[state]:
                 x += -(math.log(self.P_word_state[label[i]][sentence[i]]))
              if i+1 < len(sentence):
                  x += -(math.log(self.P_state_state[label[i]][label[i+1]]))
        return x

    # Do the training!
    #
    def train(self, data):
         P_state = {} # Probability of part of speech 
         P_word_state = {} # probability of word given a part of speech
         P_state_state = {}# probability of part of speecch given a pos
         P_start_state = {} # Probability of part of speech starting a sentence
         total_states = 0 
         for part in data:
             for i in range(0,len(part[1])):
                 state = part[1][i]
                 start_state = part[1][0]
                 total_states += 1 
                 if state in P_state :
                     P_state[state] += 1
                 else:
                     P_state[state] = 1
                     P_start_state[state] = 1
                     P_word_state[state] = {}
                     P_state_state[state]= {}
                     
                 P_start_state[start_state] += 1    
                 if (i+1)< len(part[1])and part[1][(i+1)] in P_state_state[state] :
                     P_state_state[state][part[1][i+1]] += 1
                 if  (i+1)< len(part[1]) and (part[1][(i+1)] not in P_state_state[state]) :
                     P_state_state[state][part[1][i+1]] = 1
             for word in part[0]:
                 if word in P_word_state[part[1][part[0].index(word)]]:
                     P_word_state[part[1][part[0].index(word)]][word] += 1
                 else:
                     P_word_state[part[1][part[0].index(word)]][word] = 1
                     
         for state in P_state:
             state_count = P_state[state]
             P_state[state] /= float(total_states)
             P_start_state[state] /= float(total_states)
             for next_state in P_state_state[state]:
                 P_state_state[state][next_state] /= float(state_count)
             for word in P_word_state[state] :
                 P_word_state[state][word] /= float(state_count)
         self.P_state = P_state
         self.P_start_state = P_start_state
         self.P_word_state = P_word_state
         self.P_state_state = P_state_state
         return 1
    # Functions for each algorithm.
    #Simplified
    # Probability(pos| word) =max{ Probability(word|pos) * Probability (pos)}
    def simplified(self, sentence):
        pos_sentence = [] 
        self.posterior_simplified = [1]* len(sentence)
        for word in sentence :
            final_state = ""
            max_prob = 0
            for state in self.P_state.keys():
                 if word in self.P_word_state[state] :
                     P_state_word =  self.P_state[state]*self.P_word_state[state][word]
                 else :
                     P_state_word = self.P_state[state]*0.000001
                 if P_state_word > max_prob:
                   (max_prob, final_state) = (P_state_word, state )
            self.posterior_simplified[sentence.index(word)] = max_prob       
            pos_sentence.append(final_state)
        return pos_sentence 
    # HMM _Variable Elimination
    # Forward elimination Tow table at given location i
    # Tow[i][state] += Tow[i-1][state] * Probability(state|previous_state) * Probability(word|pos)
    # Backward elimination Nu Table at word position i
    # Nu[i] += Probability(next word|next state) * Probability(next state|current state)
    # Probility(state|word) = max{Tow * Nu}
    def hmm_ve(self, sentence):
        self.posterior_ve = [None]* len(sentence)
        Tow = {}
        Tow[0] = {}
        word_0 = sentence[0]
        for state in self.P_state:
            if word_0 in self.P_word_state[state]:
               Tow[0][state] = self.P_start_state[state] * self.P_word_state[state][word_0]
            else:
               Tow[0][state] = self.P_start_state[state] * 0.00001 
               
        for i in range(1,len(sentence)):
            Tow[i] ={}  
            word = sentence[i]   
            for state in self.P_state:
                Tow[i][state] = 0  
                for state2 in self.P_state: 
                    if (word not in self.P_word_state[state]) and (state  in self.P_state_state[state2]) :
                        Tow[i][state] = Tow[i][state] + 0.000001 * self.P_state_state[state2][state] * Tow[i-1][state2]
                    if (word  in self.P_word_state[state]) and (state  not in self.P_state_state[state2]) :
                        Tow[i][state] =  Tow[i][state] + 0.0001 * self.P_word_state[state][word] * Tow[i-1][state2]    
                    if (word  not in self.P_word_state[state]) and (state  not in self.P_state_state[state2]) :
                        Tow[i][state] =  Tow[i][state] + 0.0001 * 0.000001 * Tow[i-1][state2]    
                    if (word   in self.P_word_state[state]) and (state   in self.P_state_state[state2]) :
                        Tow[i][state] =  Tow[i][state] + self.P_word_state[state][word] * self.P_state_state[state2][state] * Tow[i-1][state2]    
        
        Nu = {}
        Nu[len(sentence)-1] = {}
        for state in self.P_state:
               Nu[len(sentence)-1][state] = 1 
        for i in range(len(sentence)-2,-1,-1):
            Nu[i] = {}
            word = sentence[i+1]
            for state in self.P_state :
              Nu[i][state] = 0
              for state2 in self.P_state:
                if (word  in self.P_word_state[state2])and (state2 in self.P_state_state[state]) :
                    Nu[i][state] += self.P_state_state[state][state2] * self.P_word_state[state2][word] 
                if (word not in self.P_word_state[state2])and (state2 in self.P_state_state[state]) :
                    Nu[i][state] += self.P_state_state[state][state2] * 0.0000001 
                if (word  in self.P_word_state[state2])and (state2 not in self.P_state_state[state]) :
                    Nu[i][state] += 0.00001 * self.P_word_state[state2][word] 
                if (word not in self.P_word_state[state2])and (state2 not in self.P_state_state[state]) :
                    Nu[i][state] += 0.00001 * 0.0000001 
        pos = []           
        for i in range(0,len(sentence)):
            word =  sentence[i]
            max_prob = 0
            final_state = ''
            for state in self.P_state :
                   x = Tow[i][state] * Nu[i][state]
                   if x > max_prob : 
                       (max_prob,final_state) = (x, state)
            self.posterior_ve[i] = max_prob    
            pos.append(final_state)
        return pos    
    #HMM _ Viterbi
    # Tow table for each word position
    # Tow[first word] = emission probability * Probability of pos starting a sentence 
    # Tow [i][state] =  max{Tow[i-1]* transition probability * emission probability}
    # Once we calculate Tow values, we take max of Tow value at last position and back track to pos which 
    # caused maximum in nexr position , therby printing max likelihood sequence of part of speech
    def hmm_viterbi(self, sentence):
        self.posterior_viterbi = [1]* len(sentence)
        Tow = {}
        Tow[0] = {}
        word = sentence[0]
        max_states = {}
        for state in self.P_start_state:
            if word in self.P_word_state[state]:
               Tow[0][state] = self.P_start_state[state]*self.P_word_state[state][word]
            else:
                Tow[0][state] = self.P_start_state[state]*0.000001
        for i in range(1,len(sentence)):
            Tow[i] ={}  
            word = sentence[i]
            max_states[i] = {}
            
            for state in self.P_state:
                max_p = 0
                for state2 in self.P_state:
                  if (word in self.P_word_state[state]) and (state not in self.P_state_state[state2] ) :  
                      Tow[i][state] = Tow[i-1][state2] * self.P_word_state[state][word] * 0.0001
                  if (word not in self.P_word_state[state]) and (state in self.P_state_state[state2] ) :
                          Tow[i][state] = Tow[i-1][state2] * 0.00000001 * self.P_state_state[state2][state]
                  if (word not in self.P_word_state[state]) and (state not in self.P_state_state[state2] ) :
                          Tow[i][state] = Tow[i-1][state2] * 0.0001 * 0.00000001
                  if (word in self.P_word_state[state]) and (state in self.P_state_state[state2] ) :  
                      Tow[i][state] = Tow[i-1][state2] * self.P_word_state[state][word] * self.P_state_state[state2][state]
                  if Tow[i][state] > max_p:
                      max_p = Tow[i][state]
                      max_states[i][state] = state2
                Tow[i][state] = max_p  
        
        
        pos = ["noun"]*len(sentence)           
        max_prob = 0
        last_state = ''
        for state in self.P_state :
            if Tow[len(sentence)-1][state] > max_prob:
               (max_prob, last_state) = (Tow[len(sentence)-1][state] , state)
            self.posterior_viterbi[len(sentence)-1] = max_prob   
        pos[len(sentence)-1]= last_state
        temp = last_state
        for i in range(len(sentence)-2,-1,-1):
            pos[i] = max_states[i+1][temp]
            self.posterior_viterbi[i] = Tow[i][pos[i]]
            temp = pos[i]
        
        return pos    
  

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, algo, sentence):
        if algo == "Simplified":
            return self.simplified(sentence)
        elif algo == "HMM VE":
            return self.hmm_ve(sentence)
        elif algo == "HMM MAP":
            return self.hmm_viterbi(sentence)
        else:
            print "Unknown algo!"

