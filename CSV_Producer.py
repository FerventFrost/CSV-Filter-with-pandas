import pandas as pd
import time

class Producer:
    TimeCount = 1
    def __init__(self, ProducerQueue, FilePath, ChunkSize, MaxNumber, TimeDict):
        self.ProducerQueue = ProducerQueue
        self.FilePath = FilePath
        self.ChunkSize = ChunkSize
        self.MaxNumber = MaxNumber
        self.TimeDict = TimeDict

    def run(self): 
        df = pd.read_csv(self.FilePath, chunksize= self.ChunkSize, nrows = self.ChunkSize * self.MaxNumber, low_memory=False, usecols=[0,2,4])
        start = time.time()
        for chunk in df:
            end = time.time()
            newChunck = chunk.dropna()
            self.TimeDict["Producer"].append(end - start)
            self.TimeDict["TotalRecord"].append(newChunck.shape)
            self.ProducerQueue.put(newChunck)
            start = time.time()
            self.TimeCount+=1