from msilib.schema import File
import pandas as pd
import time

class Producer:
    def __init__(self, ProducerQueue, FilePath, ChunkSize, MaxNumber, TimeDict,Filteredby):
        self.ProducerQueue = ProducerQueue
        self.FilePath = FilePath
        self.ChunkSize = ChunkSize
        self.MaxNumber = MaxNumber
        self.Filter = Filteredby
        #benchmark
        self.TimeDict = TimeDict    

    def run(self): 
        df = pd.read_csv(self.FilePath, chunksize= self.ChunkSize, nrows = self.ChunkSize * self.MaxNumber, low_memory=False)
        #first chunk
        start = time.time()
        # extract head names to use then in filter
        Columns = pd.read_csv(self.FilePath, nrows= 5).columns

        if type(self.Filter[0]) is int:
            FileHeads = [Columns[i] for i in self.Filter]   #if Filter uses index then get names
        else:
            FileHeads = self.Filter                         #else use as it is

        for chunk in df:
            end = time.time()
            newChunck = chunk.dropna(subset= FileHeads)
            self.ProducerQueue.put(newChunck)
            #benchmark
            self.TimeDict["Producer"].append(end - start)
            self.TimeDict["TotalRecord"].append(newChunck.shape)
            start = time.time()
            
        self.ProducerQueue.put(None)