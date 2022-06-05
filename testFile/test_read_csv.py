from time import time
import pandas as pd


class IterCSV:
    def __init__(self):
        self.df = pd.read_csv(".\\2.csv", chunksize=1000, nrows=1000*5, low_memory=False)
    
    def __iter__(self):
        self.iterlist = iter(self.df)
        return self

    def __next__(self):
        try:
            print(f"Start Reading")
            start = time()
            result = next(self.iterlist)
            end = time() - start
            print(f"end Reading {end}")
            return ( end, result)
        except StopIteration:
            raise StopIteration

if __name__ == '__main__':
    dff = IterCSV()
    for i in dff:
        i

"""
start = time()
print("Start reading")
for i in df:
    end = time()
    i
    print(f"end reading {end - start}")
    start = time()
    print("Start reading")
"""