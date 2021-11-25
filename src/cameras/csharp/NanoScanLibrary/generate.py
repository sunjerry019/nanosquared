with open("Dllimports.cs", 'r') as f:
    for line in f:
        line = line.strip()
        if (line != "") and ("static extern" in line):
            print(len(line), line)