import pandas as pd
import time

class Producer:
    def __init__(self, ProducerQueue, FilePath, ChunkSize, MaxNumber, TimeDict,FileHeads):
        self.ProducerQueue = ProducerQueue
        self.FilePath = FilePath
        self.ChunkSize = ChunkSize
        self.MaxNumber = MaxNumber
        self.FileHeads = FileHeads
        #benchmark
        self.TimeDict = TimeDict    

    def run(self): 
        df = pd.read_csv(self.FilePath, chunksize= self.ChunkSize, nrows = self.ChunkSize * self.MaxNumber, low_memory=False)
        #first chunk
        start = time.time()
        
        for chunk in df:
            end = time.time()
            newChunck = chunk.dropna(subset= self.FileHeads)
            self.ProducerQueue.put(newChunck)
            #benchmark
            self.TimeDict["Producer"].append(end - start)
            self.TimeDict["TotalRecord"].append(newChunck.shape)
            start = time.time()
            
        self.ProducerQueue.put(None)