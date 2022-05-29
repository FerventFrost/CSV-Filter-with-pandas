from CSV_Main import CSVFilter


if __name__ == "__main__":
    maxNumber = 6
    FilePath = ".\\2.csv"
    BadWordPath = ".\\badWords.csv"
    chunkSize = 10000
    FilteredBy = ["JODI", "SKALA", "PO BOX 4"]
    Type = "aho"
    QueueMaxSize = 3

    Main = CSVFilter(FilePath, BadWordPath, chunkSize, maxNumber, FilteredBy, Type, QueueMaxSize)
    Main.run()
    print(f"Total Time: {Main.TotalTime}")