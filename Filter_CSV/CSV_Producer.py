import pandas as pd
import time
import threading

class Producer(threading.Thread):
    def __init__(self, ProducerQueue, FilePath, ChunkSize, MaxNumber, TimeDict,FileHeads, Lock):
        threading.Thread.__init__(self)
        self.ProducerQueue = ProducerQueue
        self.FilePath = FilePath
        self.ChunkSize = ChunkSize
        self.MaxNumber = MaxNumber
        self.FileHeads = FileHeads
        self.Lock = Lock
        self.To_MB = 1024**2
        #benchmark
        self.TimeDict = TimeDict    


    def run(self):
        #we didn't use locks here because at the end None will not be in the queue becasue lock is set so for loop will not finish
        Iterator_CSVData = IteratorCSV(self.FilePath, self.ChunkSize, self.MaxNumber, self.Lock)
        for chunk in Iterator_CSVData:
            newChunck = chunk[1].dropna(subset= self.FileHeads)
            self.ProducerQueue.put(newChunck)
            #benchmark
            self.TimeDict["Producer"].append(chunk[0])
            self.TimeDict["TotalRecord"].append(newChunck.shape)
            #chunk memmory usage + convert it to MB aup to 3 decimal places
            self.TimeDict["MemoryUsage"].append( f"{format( newChunck.memory_usage(deep=True).sum()/self.To_MB , '.3f')}MB" )
            
        self.ProducerQueue.put(None)

class IteratorCSV:
    def __init__(self, FilePath, ChunkSize, MaxNumber, Lock):
        self.File = FilePath
        self.ChunckSize = ChunkSize
        self.MaxNumber = MaxNumber
        self.Lock = Lock
        self.Data = pd.read_csv(self.File, chunksize= self.ChunckSize, nrows = self.ChunckSize * self.MaxNumber, low_memory=False)

    def __iter__(self):
        self.IterData = iter(self.Data)
        return self

    #next(x) will be used from this class because we use "self.IterData" which is Producer variable 
    def __next__(self):
        try:
            self.Lock.acquire()

            print(f"Start Reading")
            start = time.time()
            result = next(self.IterData)
            end = time.time() - start
            print(f"end Reading {end}")

            self.Lock.release()
            return (end, result)
        except StopIteration:
            self.Lock.release()
            raise StopIteration