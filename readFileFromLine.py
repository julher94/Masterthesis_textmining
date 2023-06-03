import sys
import util

# Small pythonScripts that prints the text between two lines
numOfFiles = len(sys.argv) - 1

if numOfFiles < 1:
    print("Usage: python readFileFromLine.py <file> <from_line> <to_line> <true/false extracting_keyphrases>")

else:
    # The text has to be decoded using iso-8859-1 because the default decoding of text is utf-8
    fileText = open(sys.argv[1], 'r', encoding='iso-8859-1')
    startingLine = int(sys.argv[2])
    finishLine = int(sys.argv[3])
    extractKeywords = False if sys.argv[4] == 'false' else True
    print(extractKeywords)
    textFragment = ""
    lineCounter = 0
    while lineCounter <= finishLine:
        line = fileText.readline()
        if line == "":
            break
        lineCounter += 1
        # if the user doesn't want to extract keywords, display the current line-number
        if startingLine <= lineCounter <= finishLine:
            if not extractKeywords:
                textFragment += str(lineCounter) + ": " + line
                # if keywords should be extracted append the current line without line number
                # because it would mess up the keyword extraction
            else:
                textFragment += line

    print(textFragment)
    if extractKeywords:
        print("Extract keyphrases using keyBERT:")
        print('Extracted Keywords from ' + str(sys.argv[1]) + ":\n")
        foundKeywords = util.extract_keyphrases(textFragment)
        print(foundKeywords)
        
        
        print("\nExtracted keyphrases:")
        util.extract_keyphrases(textFragment)