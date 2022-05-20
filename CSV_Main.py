from CSV_Filter import Filter
from CSV_Consumer import Consumer
from CSV_Producer import Producer
import queue
import threading
import time
import pandas as pd

class CSVFilter:
    TimeDict = {"Producer": [], "Consumer": [], "Filter": [], "TotalRecord": [], "HealthyRecord": [], "BadRecord": [], "TotalTime": []}
    TotalTime = 0
    def __init__(self, FilePath = "", BadWordPath = "", chunkSize = 100, maxNumber = 1, FilteredBy = []):
        self.FilePath = FilePath
        self.BadWordPath = BadWordPath
        self.chunkSize = chunkSize
        self.maxNumber = maxNumber
        self.FilteredBy = FilteredBy

    def check_input(self):
        if self.FilePath == "":
            print("Please input FilePath")
            return False
        elif self.BadWordPath == "":
            print("Please input BadWordPath")
            return False
        elif self.chunkSize == 0:
            print("Please input chunkSize")
            return False
        elif self.maxNumber == 0:
            print("Please input maxNumber")
            return False
        elif self.FilteredBy == []:
            print("Please input FilteredBy")
            return False
        else:
            return True

    def run(self):

        if self.check_input():

            #Create Queues
            Producer_Filter = queue.Queue()
            Filter_Counsumer = queue.Queue()
            #Create Objects
            CSVProducer = Producer(Producer_Filter, self.FilePath, self.chunkSize, self.maxNumber, self.TimeDict)
            CSVConsumer = Consumer(Filter_Counsumer, self.TimeDict)
            CSVFilter = Filter(Producer_Filter, Filter_Counsumer, self.BadWordPath, self.maxNumber, self.TimeDict)
        
            start = time.time()
            self.TimeDict["TotalTime"].append(time.time())
            #Create Thread
            producer_thread = threading.Thread(target=CSVProducer.run())
            Filter_thread = threading.Thread(target=CSVFilter.run(self.FilteredBy))
            consumer_thread = threading.Thread(target=CSVConsumer.run())
        
            #Start Thread
            producer_thread.start()
            Filter_thread.start()
            consumer_thread.start()
        
            # #Wait for Threads to Finish
            consumer_thread.join()

            end = time.time()
            self.TotalTime = self.TimeDict["TotalTime"][0]
            #Save Benchmark
            Benchmark = pd.DataFrame.from_dict(self.TimeDict, orient = 'index')
            Benchmark = Benchmark.transpose()
            Benchmark.to_csv("Benchmark.csv")