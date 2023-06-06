import sys
import util

# Use keyphrase vectorizers extracts keyphrases with part-of-speech patterns 
# from a collection of text documents and converts them into a document-keyphrase matrix
from keyphrase_vectorizers import KeyphraseCountVectorizer
# import keybert
from keybert import KeyBERT
# Import summarizer and TransformerSummarizer
from summarizer import Summarizer,TransformerSummarizer
# import every transformer to have access to all pre-trained models
from transformers import *

# script used for text summarization
numOfFiles = len(sys.argv) - 1

if numOfFiles < 1:
    print("Usage: python test.py <file>")

else:
    personA = sys.argv[2]
    personB = sys.argv[3]
    q_and_a = util.sort_by_person(personA, personB)
    questions = q_and_a[personA]
    answers = q_and_a[personB]
    
    d_tokenizer = DistilBertTokenizer.from_pretrained('bert-base-german-cased') #'distilbert-base-multilingual-cased')
    d_model = DistilBertModel.from_pretrained('bert-base-german-cased', output_hidden_states=True)
    # create a summarizer-model that uses multi-language model and tokenizer
    bert_model = Summarizer(custom_model=d_model, custom_tokenizer=d_tokenizer)
    
    print("Summarizations for all answers:")
    index = 1
    # loop through all answers
    for answer in answers:
        print('\n\nAnswer ' + str(index) + ':')
        #if index == 11:
        print(answer)
        bert_summary = ''.join(bert_model(answer, min_length=60))
        print("generated summary: ")
        print(bert_summary)
                
        index += 1
    
