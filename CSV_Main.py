from CSV_Filter import Filter
from CSV_Consumer import Consumer
from CSV_Producer import Producer
import queue
import threading
import time

if __name__ == "__main__":
    NoRows = 3
    Producer_Filter = queue.Queue()
    Filter_Counsumer = queue.Queue()
    start = time.time()

    #Create Objects
    CSVProducer = Producer(Producer_Filter, ".\\2.csv", 10**4, NoRows)
    CSVConsumer = Consumer(Filter_Counsumer)
    CSVFilter = Filter(Producer_Filter, Filter_Counsumer, ".\\badWords.csv", NoRows)
    
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
    print(f"All finshed in : {end - start}")