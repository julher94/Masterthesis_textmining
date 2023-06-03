#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 11:12:16 2023

@author: jherbst
"""
import sys
import util

# Use keyphrase vectorizers extracts keyphrases with part-of-speech patterns 
# from a collection of text documents and converts them into a document-keyphrase matrix

numOfFiles = len(sys.argv) - 1

if numOfFiles < 1:
    print("Usage: python keyPhraseExtraction.py <Interview> <PersonA> <PersonB>")

else:
    personA = sys.argv[2]
    personB = sys.argv[3]
    q_and_a = util.sort_by_person(personA, personB)
    questions = q_and_a[personA]
    answers = q_and_a[personB]
    
    
    print("Keyphrase analysis for all answers:")
    index = 1
    # loop through all answers
    for answer in answers:
        print('\n\nAnswer ' + str(index) + ':')
        print(answer)
        # extract smaller keyphrases of the current sentence
        # Get German keyphrases of the current answer
        # Use the substring from character 3 to eos in order to
        # exclude the abbreviation of the current interviewpartner
        keywords = util.extract_keyphrases(answer[3:])
        print('extracted keyphrases')
        print(keywords)
                
        index += 1
    


