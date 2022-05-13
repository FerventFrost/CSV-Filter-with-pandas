import re
import pandas as pd

class Filter:
    Iteration_counter = 1

    def __init__(self, ProducerQueue ,ConsumerQueue, BadWord_FilePath, MaxNumber):
        self.ProducerQueue = ProducerQueue
        self.ConsumerQueue = ConsumerQueue
        self.BadWord = BadWord_FilePath
        self.MaxNumber = MaxNumber

    def run(self, head):
        BadCSVWords = pd.read_csv(self.BadWord)
        BadWord = '|'.join(re.escape(x[0]) for x in BadCSVWords.values)


        while True:

            if not self.ProducerQueue.empty():

                df = self.ProducerQueue.get()
                bool_checker = df[head].str.contains(BadWord, regex = True, flags = re.I, na= False)
                self.ConsumerQueue.put( (df[~bool_checker], df[bool_checker]) )

                if self.Iteration_counter == self.MaxNumber:
                    self.ConsumerQueue.put(None)
                    break;
                self.Iteration_counter+=1 