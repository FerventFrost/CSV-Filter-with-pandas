from CSV_Filter import Filter
from CSV_Consumer import Consumer
from CSV_Producer import Producer
import queue
import threading
import time
import pandas as pd

if __name__ == "__main__":
    TimeDict = {"Producer": [], "Consumer": [], "Filter": [], "TotalRecord": [], "HealthyRecord": [], "BadRecord": [], "TotalTime": []}
    NoRows = 3
    Producer_Filter = queue.Queue()
    Filter_Counsumer = queue.Queue()
    start = time.time()

    #Create Objects
    CSVProducer = Producer(Producer_Filter, ".\\2.csv", 10**4, NoRows, TimeDict)
    CSVConsumer = Consumer(Filter_Counsumer, TimeDict)
    CSVFilter = Filter(Producer_Filter, Filter_Counsumer, ".\\badWords.csv", NoRows, TimeDict)
    
    #Create Thread
    producer_thread = threading.Thread(target=CSVProducer.run())
    Filter_thread = threading.Thread(target=CSVFilter.run(["JODI", "SKALA"]))
    consumer_thread = threading.Thread(target=CSVConsumer.run())

    #Start Thread
    producer_thread.start()
    Filter_thread.start()
    consumer_thread.start()

    #Wait for Threads to Finish
    producer_thread.join()
    Filter_thread.join()
    consumer_thread.join()

    end = time.time()
    print(f"Total Time: {end - start}")

    TimeDict["TotalTime"].append(end - start)
    Benchmark = pd.DataFrame.from_dict(TimeDict, orient = 'index')
    Benchmark = Benchmark.transpose()
    Benchmark.to_csv("Benchmark.csv")