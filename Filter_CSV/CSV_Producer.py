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
        #benchmark
        self.TimeDict = TimeDict    


    def run(self): 
        Iterator_CSVData = IteratorCSV(self.FilePath, self.ChunkSize, self.MaxNumber)
        for chunk in Iterator_CSVData:
            newChunck = chunk[1].dropna(subset= self.FileHeads)
            self.ProducerQueue.put(newChunck)
            #benchmark
            self.TimeDict["Producer"].append(chunk[0])
            self.TimeDict["TotalRecord"].append(newChunck.shape)
            
        self.ProducerQueue.put(None)

class IteratorCSV:
    def __init__(self, FilePath, ChunkSize, MaxNumber):
        self.File = FilePath
        self.ChunckSize = ChunkSize
        self.MaxNumber = MaxNumber
        self.Data = pd.read_csv(self.File, chunksize= self.ChunckSize, nrows = self.ChunckSize * self.MaxNumber, low_memory=False)

    def __iter__(self):
        self.IterData = iter(self.Data)
        return self

    #next(x) will be used from this class because we use "self.IterData" which is Producer variable 
    def __next__(self):
        try:
            print(f"Start Reading")
            start = time.time()
            result = next(self.IterData)
            end = time.time() - start
            print(f"end Reading {end}")
            return (end, result)
        except StopIteration:
            raise StopIteration