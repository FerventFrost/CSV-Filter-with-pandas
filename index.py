from CSV_Main import CSVFilter


if __name__ == "__main__":
    maxNumber = 6
    FilePath = ".\\2.csv"
    BadWordPath = ".\\badWords.csv"
    chunkSize = 10000
    FilteredBy = [0, 1, 2]
    Type = "aho"

    Main = CSVFilter(FilePath, BadWordPath, chunkSize, maxNumber, FilteredBy, Type)
    Main.run()
    print(f"Total Time: {Main.TotalTime}")