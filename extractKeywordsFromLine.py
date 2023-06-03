import sys
import util

# Small pythonScripts that prints the text between two lines
numOfFiles = len(sys.argv) - 1

if numOfFiles < 1:
    print("Usage: python readFileFromLine.py <file> <from_line> <to_line> <true/false extracting_keyphrases>")

else:
    # get the text provide by the utility-function
    extractKeywords = False if sys.argv[4] == 'false' else True
    textPassage = util.read_file_from_line(sys.argv[1], sys.argv[2], sys.argv[3], extractKeywords)
    print("\n\n")
    print(textPassage)
    print("\n\n")
    if extractKeywords:
        print("Please enter the parameters for the keyword extraction:")
        print("<Number_of_keywords> <ngram_min> <ngram_max>")
        print("Enter the number of keywords to be extracted:")
        numTopKeywords = int(input())
        print("Enter the n-gram-minimum:")
        n_gram_min = int(input())
        print("Enter the n-gram-maximum:")
        n_gram_max = int(input())
        util.keyword_by_bert(textPassage, numTopKeywords, n_gram_min, n_gram_max)
        
        print("\nExtracted keyphrases:")
        print(util.extract_keyphrases(textPassage))