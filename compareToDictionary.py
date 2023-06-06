import sys
import util
import nltk

# Small pythonScript to search a text for every word in the provided dictionary (textfile)
if len(sys.argv) <= 1:
    print("Usage: python readFileFromLine.py <file> <from_line> <to_line>")

else:
    # content holds the text from the interview while
    # dictionary is a list that contains all the search terms
    content_lines = util.read_line_by_line()
    dictionary_reader = open(sys.argv[2], 'r')
    dictionary_list = dictionary_reader.read().lower().strip('\n').split(',')
    print("current dictionary: " + str(dictionary_list))
    word_frequency = 0
    # iterate through the lines read from the file
    for line in content_lines:
        # split each line into its words
        words = line.split()
        # after that iterate through the list of words and compare each word
        # with the dictionary provided in the arguments
        for word in words:
            stripped_word = word.strip('\n').lower()
            if stripped_word in dictionary_list:
                print("Match! The word " + stripped_word + "  was found in line " + str(content_lines.index(line)))

        #word_frequency = nltk.FreqDist(words)
        #print("Word frequency: " + str(word_frequency.most_common()))



