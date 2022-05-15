import re
import time
import pandas as pd
from CSV_Trie import Trie

class Filter:
    Iteration_counter = 1
    TrieOBJ = Trie()

    def __init__(self, ProducerQueue ,ConsumerQueue, BadWord_FilePath, MaxNumber, TimeDict):
        self.ProducerQueue = ProducerQueue
        self.ConsumerQueue = ConsumerQueue
        self.BadWord = BadWord_FilePath
        self.MaxNumber = MaxNumber
        #benchmark
        self.TimeDict = TimeDict    

    def MakeTrie(self):
        
        BadCSVWords = pd.read_csv(self.BadWord)
        for word in BadCSVWords.values:
            self.TrieOBJ.insert(word[0])
        return Trie

    def MakeWordList_UsingRegex(self):
        BadCSVWords = pd.read_csv(self.BadWord)
        BadWord = '|'.join(re.escape(x[0]) for x in BadCSVWords.values)
        return BadWord

    #Get List of Bools and return False if one of them is False
    def Return_True_False(self, BoolList):
        x = BoolList[0]
        for i in BoolList:
            x = x & i
        return x
    
    def FilterByRegEx(self, Heads):
        boolList = []
        Badwords = self.MakeWordList_UsingRegex()

        while True:

            if not self.ProducerQueue.empty():
                df = self.ProducerQueue.get()

                start = time.time()
                #Filter by multiple columns and save it in list
                #Use "~" to change True to False and False to True 
                #we change True to False because we want to filter bad words
                if type(Heads[0]) is str:
                    boolList = [ ~df[head].str.contains(Badwords, regex = True, flags = re.I, na= False) for head in Heads ]
                else:
                    boolList = [ ~df.iloc[:,head].str.contains(Badwords, regex = True, flags = re.I, na= False) for head in Heads ]
                bool_checker = self.Return_True_False(boolList)

                end = time.time()
                healthy_df = df[bool_checker]
                bad_df = df[~bool_checker]
                self.ConsumerQueue.put( (healthy_df, bad_df) )

                #Benchmark
                self.TimeDict["Filter"].append(end - start)
                self.TimeDict["HealthyRecord"].append(healthy_df.shape)
                self.TimeDict["BadRecord"].append(bad_df.shape)
                if self.Iteration_counter == self.MaxNumber:
                    self.ConsumerQueue.put(None)
                    break;
                self.Iteration_counter+=1 
                #clear List for next iteration
                boolList.clear()
        #if you want to use fitler class again
        self.Iteration_counter = 1

    def FilterByTrie(self, Heads):
        boolList = []
        self.MakeTrie()

        while True:

            if not self.ProducerQueue.empty():

                df = self.ProducerQueue.get()

                start = time.time()
                #Filter by multiple columns and save it in list
                #Use "~" to change True to False and False to True 
                #we change True to False because we want to filter bad words
                if type(Heads[0]) is str:
                    boolList = [ ~df[head].apply(self.TrieOBJ.PartialSearch) for head in Heads ]
                else:
                    boolList = [ ~df.iloc[:,head].apply(self.TrieOBJ.PartialSearch) for head in Heads ]

                bool_checker = self.Return_True_False(boolList)

                end = time.time()

                healthy_df = df[bool_checker]
                bad_df = df[~bool_checker]
                self.ConsumerQueue.put( (healthy_df, bad_df) )

                #Benchmark
                self.TimeDict["Filter"].append(end - start)
                self.TimeDict["HealthyRecord"].append(healthy_df.shape)
                self.TimeDict["BadRecord"].append(bad_df.shape)

                if self.Iteration_counter == self.MaxNumber:
                    self.ConsumerQueue.put(None)
                    break;
                self.Iteration_counter+=1 
                #clear List for next iteration
                boolList.clear()
        #if you want to use fitler class again
        self.Iteration_counter = 1

    def run(self, Heads):
        self.FilterByTrie(Heads)