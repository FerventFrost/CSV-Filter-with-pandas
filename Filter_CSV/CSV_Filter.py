import re
import time
import threading
import pandas as pd
from .CSV_Trie import Trie      #dot (.) to access file in the current directory
import ahocorasick

class Filter(threading.Thread):
    Iteration_counter = 1
    TrieOBJ = Trie()
    automaton = ahocorasick.Automaton()

    def __init__(self, ProducerQueue ,ConsumerQueue, BadWord_FilePath, TimeDict, Heads, Type):
        threading.Thread.__init__(self)
        self.ProducerQueue = ProducerQueue
        self.ConsumerQueue = ConsumerQueue
        self.BadWord = BadWord_FilePath
        self.Heads = Heads
        self.Type = Type
        self.df = 0
        self.boolList = []
        #benchmark
        self.TimeDict = TimeDict    

    def MakeTrie(self):
        
        BadCSVWords = pd.read_csv(self.BadWord)
        for word in BadCSVWords.values:
            self.TrieOBJ.insert(word[0].lower())
        return self.TrieOBJ

    def MakeWordList_UsingRegex(self):
        BadCSVWords = pd.read_csv(self.BadWord)
        BadWord = '|'.join(re.escape(x[0]) for x in BadCSVWords.values)
        return BadWord

    def MakeTrie_UsingPyAcho(self):
        BadCSVWords = pd.read_csv(self.BadWord).values
        for word in BadCSVWords:
            self.automaton.add_word(word[0].lower(), word[0].lower())
        return self.automaton
   
    #Get List of Bools and return False if one of them is False
    def Return_True_False(self, BoolList):
        x = BoolList[0]
        for i in BoolList:
            x = x & i
        return x
    
    #Filter by multiple columns and save it in list
    #Use "~" to change True to False and False to True 
    #we change True to False because we want to filter bad words
    def FilterByRegEx(self, Heads, Badwords):
        self.boolList = [ ~self.df[head].str.contains(Badwords, regex = True, flags = re.I, na= False) for head in Heads ]
        bool_checker = self.Return_True_False(self.boolList)
        #clear List for next iteration
        self.boolList.clear()
        return bool_checker

    def FilterByTrie(self, Heads):
        self.boolList = [ ~self.df[head].apply(self.TrieOBJ.Custom_AhoCorasick) for head in Heads ]
        bool_checker = self.Return_True_False(self.boolList)
        #clear List for next iteration
        self.boolList.clear()
        return bool_checker

    def FilterByAho(self, Heads):
        self.boolList = [ ~self.df[head].apply(lambda x : len(list(self.automaton.iter(x.lower()))) != 0) for head in Heads ]
        bool_checker = self.Return_True_False(self.boolList)
        #clear List for next iteration
        self.boolList.clear()
        return bool_checker
    
    def FilterBy(self):
        if self.Type == "regex":
            Badwords = self.MakeWordList_UsingRegex()
        elif self.Type == "aho":
            self.MakeTrie_UsingPyAcho()
            self.automaton.make_automaton()
        else:
            self.MakeTrie()

        while True:
            if not self.ProducerQueue.empty():
                self.df = self.ProducerQueue.get()

                if self.df is None:
                    self.ConsumerQueue.put(None)
                    break

                start = time.time()
                #Filter by multiple columns and save it in list
                #Use "~" to change True to False and False to True 
                #we change True to False because we want to filter bad words

                if self.Type == "regex":
                    print("regex")
                    bool_checker = self.FilterByRegEx(self.Heads, Badwords)
                elif self.Type == "aho":
                    print("aho")
                    bool_checker = self.FilterByAho(self.Heads)
                else:
                    print("custom")
                    bool_checker = self.FilterByTrie(self.Heads)

                end = time.time()

                healthy_df = self.df[bool_checker]
                bad_df = self.df[~bool_checker]
                self.ConsumerQueue.put( (healthy_df, bad_df) )

                #Benchmark
                self.TimeDict["Filter"].append(end - start)
                self.TimeDict["HealthyRecord"].append(healthy_df.shape)
                self.TimeDict["BadRecord"].append(bad_df.shape)

    def run(self):
        self.FilterBy()