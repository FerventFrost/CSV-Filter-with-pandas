import pandas as pd
import time

class Producer:
    def __init__(self, ProducerQueue, FilePath, ChunkSize, MaxNumber, TimeDict):
        self.ProducerQueue = ProducerQueue
        self.FilePath = FilePath
        self.ChunkSize = ChunkSize
        self.MaxNumber = MaxNumber
        #benchmark
        self.TimeDict = TimeDict    

    def run(self): 
        df = pd.read_csv(self.FilePath, chunksize= self.ChunkSize, nrows = self.ChunkSize * self.MaxNumber, low_memory=False, usecols=[0,2,4])
        #first chunk
        start = time.time()
        for chunk in df:
            end = time.time()
            print(f"Prodcure: {self.ProducerQueue.qsize()}")
            newChunck = chunk.dropna()
            self.ProducerQueue.put(newChunck)
            #benchmark
            self.TimeDict["Producer"].append(end - start)
            self.TimeDict["TotalRecord"].append(newChunck.shape)
            start = time.time()
            
        self.ProducerQueue.put(None)