from Filter_CSV.CSV_Main import CSVFilter


if __name__ == "__main__":
    maxNumber = 20
    FilePath = ".\\2.csv"
    BadWordPath = ".\\badWords.csv"
    chunkSize = 10**4*5
    FilteredBy = [0, 2, 4]
    Type = "aho"
    QueueMaxSize = 5
    BenchMark_FileName = "Benchmark"
    Healthy_FileName = "Healthy"
    Bad_FileName = "Unhealthy"
    
    Main = CSVFilter(FilePath, BadWordPath, chunkSize, maxNumber, FilteredBy, Type, QueueMaxSize, BenchMark_FileName, Healthy_FileName, Bad_FileName)
    Main.run()
    print(f"Total Time: {Main.TotalTime}")