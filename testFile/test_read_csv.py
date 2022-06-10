from time import sleep, time
import pandas as pd
import threading
import queue

class IterCSV:
    def __init__(self, lock):
        self.df = pd.read_csv(".\\2.csv", chunksize=10**4*5, nrows=10**4*10, low_memory=False)
        self.Lock = lock
    
    def __iter__(self):
        self.iterlist = iter(self.df)
        return self

    def __next__(self):
        try:
            self.Lock.acquire()

            start = time()
            result = next(self.iterlist)
            end = time() - start
            print(f"Reading Time {end}")
            self.Lock.release()

            return ( end, result)
        except StopIteration:
            self.Lock.release()
            raise StopIteration
            
        
class run(threading.Thread):
    def __init__(self, q, lock):
        threading.Thread.__init__(self)
        self.q = q
        self.Lock = lock

    def run(self):
        it = IterCSV(self.Lock)
        for i in it:
            print("Put Stage\n")
            self.q.put(i)
        self.q.put(None)

class nothing(threading.Thread):
    def __init__(self, q, lock):
        threading.Thread.__init__(self)
        self.q = q
        self.Lock = lock
    
    def run(self):
        iteration_time = 0
        while True:
            iteration_time += 1
            
            var = self.q.get()
            with self.Lock:
                print(f"    Number of Iteartions: {iteration_time} ")
                iteration_time = 0

                if var == None:
                    break
                print(format(var[1].memory_usage(deep=True).sum() / (1024 **2), '.3f'))
                s = time()
                for _ in range(10**8):
                    pass
                print(f"    Sleep time {time() - s}")



if __name__ == '__main__':
    threadLock = threading.Lock()
    q = queue.Queue(4)
    dff = run(q, threadLock)
    nt = nothing(q, threadLock)
    start = time()
    dff.start()
    nt.start()

    dff.join()
    nt.join()
    print(f"total time is: {time() - start}")


"""
if __name__ == '__main__':
    threadLock = threading.Lock()
    hi = IterCSV(threadLock)
    start = time()
    for i in hi:
        i
    print(f"total time is: {time() - start}")
"""