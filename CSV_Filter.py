import re
import pandas as pd
from CSV_Trie import Trie

class Filter:
    Iteration_counter = 1
    TrieOBJ = Trie()

    def __init__(self, ProducerQueue ,ConsumerQueue, BadWord_FilePath, MaxNumber):
        self.ProducerQueue = ProducerQueue
        self.ConsumerQueue = ConsumerQueue
        self.BadWord = BadWord_FilePath
        self.MaxNumber = MaxNumber

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
    
    def run(self, Heads):
        self.TrieOBJ.CaseSensitive = True
        boolList = []
        self.MakeTrie()


        while True:

            if not self.ProducerQueue.empty():

                df = self.ProducerQueue.get()


                """
                # for head in Heads:
                bool_checker =  df[Heads].str.contains(Maded_Trie, regex = True, flags = re.I, na= False)
                self.ConsumerQueue.put( (df[~bool_checker], df[bool_checker]) )
                """
                print(type(Heads))
                for head in Heads:
                    boolList.append( df[head].apply(self.TrieOBJ.PartialSearch) )

                bool_checker = self.Return_True_False(boolList)


                self.ConsumerQueue.put( (df[~bool_checker], df[bool_checker]) )

                if self.Iteration_counter == self.MaxNumber:
                    self.ConsumerQueue.put(None)
                    break;
                self.Iteration_counter+=1 
                boolList.clear()