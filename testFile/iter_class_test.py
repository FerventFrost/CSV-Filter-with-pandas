from time import time
import pandas as pd

class Test_Iter:
    def __init__(self):
        self.li = [1,2,3,4,5]

    def __iter__(self):
        #Make List iterable
        return iter(self.li)

    def __next__(self):
        try:
            #Then iter throw it
            return next(self.li)
        except StopIteration:
            raise StopIteration
    
    def sum(self):
        sum = 0
        class_array = Test_Iter()
        for i in class_array:
            sum +=i
        return sum

class readcsv_Iter:
    def __init__(self):
        self.Data = pd.read_csv("testFile/annual-enterprise.csv", chunksize= 50, nrows = 50 * 3)
        self.DisplayData = pd.read_csv("testFile/annual-enterprise.csv", chunksize= 50, nrows = 50 * 3)
    
    def __iter__(self):
        #if we use the same example above it won't work because we need to send read time with it
        #to solve it we make a iter_list to hold data and iter throw it 
        self.IterData = iter(self.Data)
        return self
        # return iter(self.Data)
        

    def __next__(self):
        try: 
            #Send result as tuple
            start = time()
            PdIter = next(self.IterData)
            result = (time() - start, PdIter)
            return result
        except StopIteration:
            raise StopIteration

    def display(self):
        start = time()
        for i in self.DisplayData:
            i
        print(f"Display Functio time: {time() - start}")



"""
if __name__ == '__main__':
    hi = Test_Iter()
    sum = hi.sum()
    print(sum)
    mm = iter(hi)
    print(type(mm))
    print(next(mm))
    print(next(mm))
    print(next(mm))
    print(next(mm))
    print(next(mm))
"""

if __name__ == '__main__':
    Data = readcsv_Iter()
    start = time()
    Data_iter = iter(Data)
    
    print(next(Data_iter)[0])
    print(next(Data_iter)[0])
    print(next(Data_iter)[0])
    print(f"Total Time : {time() - start}")

    Data.display()
