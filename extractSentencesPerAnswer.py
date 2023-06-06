#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 13:01:59 2023

@author: jherbst
"""

import sys
import util

# this script gets an interview (as txt-file) and the two abbreviations of the interviewer and interviewee as parameters
# and extracts all questions and all answers from the given interview according to the given abbreviations
# After that Bert is used to extract keywords/sentences, that will be used for coding the interviews
numOfFiles = len(sys.argv) - 1

if numOfFiles < 1:
    print("Usage: python extractSentencesPerAnswer.py <textfile> <Person_A> <Person_B>")

else:
    personA = sys.argv[2]
    personB = sys.argv[3]
    q_and_a = util.sort_by_person(personA, personB)
    questions = q_and_a[personA]
    answers = q_and_a[personB]
    
    print("Keyword analysis for all answers:")
    index = 0
    for answer in answers:
        print('\n\nAnswer ' + str(index) + ':')
        print(answer)

        print("Summarize this answer?: y/n")
        inp = input()
        if inp == "y":
            util.summarize(answer)
        
            
        # ask the user if the keywords for the whole answer should be extracted
        print("\nExtract keywords for the current answer?: y/n")
        inp = input()
        if inp == "y":
            # if so, ask for the parameters for the number of keywords and the n-gram-range
            print("Please enter the parameters for the keyword extraction:")
            print("<Number_of_keywords> <ngram_min> <ngram_max>")
            print("Enter the number of keywords to be extracted:")
            numTopKeywords = int(input())
            print("Enter the n-gram-minimum:")
            n_gram_min = int(input())
            print("Enter the n-gram-maximum:")
            n_gram_max = int(input())
            print("\n")
            # start with the substring from 3 to end of string to exclude the abbreviations
            # at the beginning of each paragraph
            util.keyword_by_bert(answer[3:-13], numTopKeywords, n_gram_min, n_gram_max)
            print("\n")
            
        # ask the user if the answer should be split up into its sentences
        print("\nSplit current answer into sentences?: y/n")
        inp = input()
        if inp == "y":
            print("\n")
            print("\n")
            sentences = util.get_sentences(answer)
            # print every senteces followed by the question if the keywords
            # should be extracted for this sentence. If so, ask the user to provide
            # parameters for the number of keywords and n-gram-range
            sentence_nr = 1
            for sentence in sentences:
                print("Sentence number " + str(sentence_nr))
                print(sentence)
                print("extract keywords for this sentence?: y/n")
                inp = input()
                if inp == "y":
                    print("\n")
                    print("Please enter the parameters for the keyword extraction:")
                    print("<Number_of_keywords> <ngram_min> <ngram_max>")
                    print("Enter the number of keywords to be extracted:")
                    numTopKeywords = int(input())
                    print("Enter the n-gram-minimum:")
                    n_gram_min = int(input())
                    print("Enter the n-gram-maximum:")
                    n_gram_max = int(input())
                    print("\n")
                    util.keyword_by_bert(sentence, numTopKeywords, n_gram_min, n_gram_max)
                    print("\n")
                    # increment the counter for the sentences 1 by one  
                sentence_nr += 1
            
            
            
        
            
        # increment the index for the current 1 by one            
        index += 1

            
        
        
        