from CSV_Main import CSVFilter
import time


if __name__ == "__main__":
    maxNumber = 3
    FilePath = ".\\2.csv"
    BadWordPath = ".\\badWords.csv"
    chunkSize = 10**4
    FilteredBy = ["JODI", "SKALA", "PO BOX 4"]


    start = time.time()
    Main = CSVFilter(FilePath, BadWordPath, chunkSize, maxNumber, FilteredBy)
    Main.run()
    end = time.time()
    print(f"Total Time: {end - start}")
