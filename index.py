from Filter_CSV.CSV_Main import CSVFilter


if __name__ == "__main__":
    maxNumber = 6
    FilePath = ".\\2.csv"
    BadWordPath = ".\\badWords.csv"
    chunkSize = 1000
    FilteredBy = [0, 2, 4]
    Type = "aho"
    QueueMaxSize = 3
    BenchMark_FileName = "Benchmark"
    Healthy_FileName = "Healthy"
    Bad_FileName = "Unhealthy"
    
    Main = CSVFilter(FilePath, BadWordPath, chunkSize, maxNumber, FilteredBy, Type, QueueMaxSize, BenchMark_FileName, Healthy_FileName, Bad_FileName)
    Main.run()
    print(f"Total Time: {Main.TotalTime}")