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

                for head in Heads:
                    boolList.append( df[head].str.contains(Badwords, regex = True, flags = re.I, na= False) )

                bool_checker = self.Return_True_False(boolList)

                end = time.time()
                self.TimeDict["Filter"].append(end - start)
                
                self.ConsumerQueue.put( (df[~bool_checker], df[bool_checker]) )

                if self.Iteration_counter == self.MaxNumber:
                    self.ConsumerQueue.put(None)
                    break;

                self.Iteration_counter+=1 
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

                for head in Heads:
                    boolList.append( df[head].apply(self.TrieOBJ.PartialSearch) )
                bool_checker = self.Return_True_False(boolList)

                end = time.time()

                healthy_df = df[~bool_checker]
                bad_df = df[bool_checker]
                self.TimeDict["Filter"].append(end - start)
                self.TimeDict["HealthyRecord"].append(healthy_df.shape)
                self.TimeDict["BadRecord"].append(bad_df.shape)

                self.ConsumerQueue.put( (healthy_df, bad_df) )
                if self.Iteration_counter == self.MaxNumber:
                    self.ConsumerQueue.put(None)
                    break;

                self.Iteration_counter+=1 
                boolList.clear()

        #if you want to use fitler class again
        self.Iteration_counter = 1

    def run(self, Heads):
        self.FilterByTrie(Heads)