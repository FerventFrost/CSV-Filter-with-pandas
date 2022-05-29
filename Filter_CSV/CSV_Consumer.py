import time

class Consumer:

    def __init__(self, ConsumerQueue, FileNames, TimeDict):
        self.ConsumerQueue = ConsumerQueue
        self.FileNames = FileNames
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
                message[0].to_csv(f"{self.FileNames[0]}.csv", mode = 'a', index = False)
                message[1].to_csv(f"{self.FileNames[1]}.csv", mode = 'a', index = False)

                end = time.time()
                #benchmark
                self.TimeDict["Consumer"].append(end - start)
        #Global start time - current end time
        self.TimeDict["TotalTime"][0] = time.time() - self.TimeDict["TotalTime"][0]