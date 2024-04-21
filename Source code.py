from MFIS_Read_Functions import *

def main():
    # Read the fuzzy sets file
    fuzzySetsDict = readFuzzySetsFile('Files/InputVarSets.txt')
    fuzzySetsDict.printFuzzySetsDict()

if __name__ == '__main__':
    main()