import pandas as pd

class Producer:

    def __init__(self, ProducerQueue, FilePath, ChunkSize, MaxNumber):
        self.ProducerQueue = ProducerQueue
        self.FilePath = FilePath
        self.ChunkSize = ChunkSize
        self.MaxNumber = MaxNumber

    def run(self): 
        df = pd.read_csv(self.FilePath, chunksize= self.ChunkSize, nrows = self.ChunkSize * self.MaxNumber, low_memory=False, usecols=[0,2,4])
        for chunk in df:
            self.ProducerQueue.put(chunk.dropna())
