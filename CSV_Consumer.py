import time
class Consumer:

    def __init__(self, ConsumerQueue, TimeDict):
        self.ConsumerQueue = ConsumerQueue
        #benchmark
        self.TimeDict = TimeDict

    def run(self):
        while True:

            if not self.ConsumerQueue.empty():
                message = self.ConsumerQueue.get()

                #if no more chuncks to read from producer
                if message is None:
                    break

                start = time.time()  
                #save to file  
                message[0].to_csv("Healthy_filtered_words.csv", mode = 'a', index = False)
                message[1].to_csv("Bad_filtered_words.csv", mode = 'a', index = False)

                end = time.time()
                #benchmark
                self.TimeDict["Consumer"].append(end - start)
        #Global start time - current end time
        self.TimeDict["TotalTime"][0] = time.time() - self.TimeDict["TotalTime"][0]