import re
import pandas as pd
from Trie import Trie

class Filter:
    Iteration_counter = 1

    def __init__(self, ProducerQueue ,ConsumerQueue, BadWord_FilePath, MaxNumber):
        self.ProducerQueue = ProducerQueue
        self.ConsumerQueue = ConsumerQueue
        self.BadWord = BadWord_FilePath
        self.MaxNumber = MaxNumber

    def MakeTrie(self):
        Trie = Trie()
        BadCSVWords = pd.read_csv(self.BadWord)
        for word in BadCSVWords.values:
            Trie.insert(word[0])
        return Trie

    def MakeWordList_UsingRegex(self):
        BadCSVWords = pd.read_csv(self.BadWord)
        BadWord = '|'.join(re.escape(x[0]) for x in BadCSVWords.values)
        return BadWord


    def run(self, head):
        Trie = self.MakeTrie()


        while True:

            if not self.ProducerQueue.empty():

                df = self.ProducerQueue.get()
                # bool_checker = df[head].str.contains(BadWord, regex = True, flags = re.I, na= False)
                bool_checker = df[head].str.contains(Trie.search, regex = True, flags = re.I, na= False)
                self.ConsumerQueue.put( (df[~bool_checker], df[bool_checker]) )

                if self.Iteration_counter == self.MaxNumber:
                    self.ConsumerQueue.put(None)
                    break;
                self.Iteration_counter+=1 