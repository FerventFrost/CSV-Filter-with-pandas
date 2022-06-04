import imp
import pandas as pd
import time
import threading

class Producer(threading.Thread):
    def __init__(self, ProducerQueue, FilePath, ChunkSize, MaxNumber, TimeDict,FileHeads):
        threading.Thread.__init__(self)
        self.ProducerQueue = ProducerQueue
        self.FilePath = FilePath
        self.ChunkSize = ChunkSize
        self.MaxNumber = MaxNumber
        self.FileHeads = FileHeads
        self.Data = pd.read_csv(self.FilePath, chunksize= self.ChunkSize, nrows = self.ChunkSize * self.MaxNumber, low_memory=False)
        #benchmark
        self.TimeDict = TimeDict    

    def __iter__(self):
        self.IterData = iter(self.Data)
        return self

    def __next__(self):
        try:
            start = time.time()
            result = next(self.IterData)
            return ( time.time() - start, result)
        except StopIteration:
            raise StopIteration

    def run(self): 
        # df = pd.read_csv(self.FilePath, chunksize= self.ChunkSize, nrows = self.ChunkSize * self.MaxNumber, low_memory=False)
        #first chunk
        start = time.time()
        
        for chunk in self.Data:
            end = time.time()
            newChunck = chunk.dropna(subset= self.FileHeads)
            self.ProducerQueue.put(newChunck)
            #benchmark
            self.TimeDict["Producer"].append(end - start)
            self.TimeDict["TotalRecord"].append(newChunck.shape)
            start = time.time()
            
        self.ProducerQueue.put(None)