import sys
import util

# this script gets an interview (as txt-file) and the two abbreviations of the interviewer and interviewee as parameters
# and extracts all questions and all answers from the given interview according to the given abbreviations
# After that Bert is used to extract keywords/sentences, that will be used for coding the interviews
numOfFiles = len(sys.argv) - 1

if numOfFiles < 1:
    print("Usage: python readFileFromLine.py <file>")

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
        if index == 11:
            sentences = util.get_sentences(answer)
            sentences.pop()
            for sentence in sentences:
                util.extract_keywords_from(sentence)
        index += 1