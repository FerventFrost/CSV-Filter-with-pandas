import time
class Consumer:

    def __init__(self, ConsumerQueue, TimeDict):
        self.ConsumerQueue = ConsumerQueue
        self.TimeDict = TimeDict

    def run(self):
        while True:

            if not self.ConsumerQueue.empty():
                message = self.ConsumerQueue.get()

                if message is None:
                    break
                start = time.time()    
                message[0].to_csv("Healthy_filtered_words.csv", mode = 'a', index = False)
                message[1].to_csv("Bad_filtered_words.csv", mode = 'a', index = False)
                end = time.time()
                self.TimeDict["Consumer"].append(end - start)