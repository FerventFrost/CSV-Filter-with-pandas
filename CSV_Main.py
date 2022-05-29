from re import I
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
    def __init__(self, FilePath = "", BadWordPath = "", chunkSize = 100, maxNumber = 1, FilteredBy = [], Type = "", QueueMaxSize = 0, BenchmarkFileName = "Benchmark", HealthyFileName = "Healthy", UnheathlyFileName = "Unheathly"):
        self.FilePath = FilePath
        self.BadWordPath = BadWordPath
        self.chunkSize = chunkSize
        self.maxNumber = maxNumber
        self.FilteredBy = FilteredBy
        self.Type = Type
        self.QMaxSize = QueueMaxSize
        self.Benchmark = BenchmarkFileName
        self.Healthy = HealthyFileName
        self.Unheathly = UnheathlyFileName

        # extract head names to use then in filter
        Columns = pd.read_csv(self.FilePath, nrows= 5).columns

        if type(self.FilteredBy[0]) is int:
            self.FileHeads = [Columns[i] for i in self.FilteredBy]   #if Filter uses index then get names
        else:
            self.FileHeads = self.FilteredBy                         #else use as it is


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
            Producer_Filter = queue.Queue(maxsize=self.QMaxSize)
            Filter_Counsumer = queue.Queue(maxsize=self.QMaxSize)
            #Create Objects
            CSVProducer = Producer(Producer_Filter, self.FilePath, self.chunkSize, self.maxNumber, self.TimeDict, self.FileHeads)
            CSVConsumer = Consumer(Filter_Counsumer, [self.Healthy, self.Unheathly], self.TimeDict)
            CSVFilter = Filter(Producer_Filter, Filter_Counsumer, self.BadWordPath, self.TimeDict, self.FileHeads, self.Type)
        
            #start program time
            self.TimeDict["TotalTime"].append(time.time())
            #Create Thread
            producer_thread = threading.Thread(target=CSVProducer.run)
            Filter_thread = threading.Thread(target=CSVFilter.run)
            consumer_thread = threading.Thread(target=CSVConsumer.run)
        
            #Start Thread
            producer_thread.start()
            Filter_thread.start()
            consumer_thread.start()
        
            # #Wait for Threads to Finish
            consumer_thread.join()

            #save total time in the var.
            self.TotalTime = self.TimeDict["TotalTime"][0]
            #Save Benchmark
            Benchmark = pd.DataFrame.from_dict(self.TimeDict, orient = 'index')
            Benchmark = Benchmark.transpose()
            Benchmark.to_csv(f"{self.Benchmark}.csv")