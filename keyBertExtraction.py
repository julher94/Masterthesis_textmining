#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 13:30:29 2023

@author: jherbst
"""
import sys
import util

# this script gets an interview (as txt-file) and the two abbreviations of the interviewer and interviewee as parameters
# and extracts all questions and all answers from the given interview according to the given abbreviations
# After that Bert is used to extract keywords/sentences, that will be used for coding the interviews
numOfFiles = len(sys.argv) - 1

if numOfFiles < 1:
    print("Usage: python keyBertExtraction.py <textfile> <Person_A> <Person_B> <Number_of_keywords> <ngram_min> <ngram_max>")

else:
    personA = sys.argv[2]
    personB = sys.argv[3]
    numKeywords = sys.argv[4]
    n_gram_min = sys.argv[5]
    n_gram_max = sys.argv[6]
    q_and_a = util.sort_by_person(personA, personB)
    questions = q_and_a[personA]
    answers = q_and_a[personB]

    print("Keyword analysis for all answers:")
    index = 0
    for answer in answers:
        print('\n\nAnswer ' + str(index) + ':')
        print(answer[3:-13])
        # start with the substring from 3 to end of string to exclude the abbreviations
        # at the beginning of each paragraph
        util.keyword_by_bert(answer[3:-13], int(numKeywords), int(n_gram_min), int(n_gram_max))
        index += 1
