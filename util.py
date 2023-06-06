import re
import sys


# Small pythonScript that reads all text line by line form a textfile and saves them into a list
# so every line of the text and its index is saved
def read_line_by_line():
    # the files have to opened using iso-8859-1-encoding, because the default encoding with utf-8 doesn't work
    return open(sys.argv[1], 'r', encoding='iso-8859-1').readlines()


# Function reads text as bloc from a file and not line by line
def read_all():

    if len(sys.argv) > 1:
        # the files have to opened using iso-8859-1-encoding, because the default encoding with utf-8 doesn't work
        text = open(sys.argv[1], 'r', encoding='iso-8859-1').read().split()
        return text

    else:
        print("No textfile found")
        
def read_file_from_line(file, start, end, extractKeywords):

    # The text has to be decoded using iso-8859-1 because the default decoding of text is utf-8
    fileText = open(file, 'r', encoding='iso-8859-1')
    # fileText, startingline, finishline are arguments provided by the console(string), therefore they all have to be
    # converted into the necessary datatypes
    startingLine = int(start)
    finishLine = int(end)
    # define a variable that will contain the text and a counter for the line
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
                
    return textFragment


# Function takes a text/text fragment and extracts/scores the keywords using rake
def extract_keywords_from(text):

    import nltk
    nltk.download('stopwords')
    nltk.download('punkt')
    from rake_nltk import Rake
    print("Extracting keywords using rake:")
    r = Rake(language="german")
    r.extract_keywords_from_text(text)
    print(r.get_word_frequency_distribution())


# utility function that returns a list with all questions and all answers
def sort_by_person(person_a, person_b):

    if len(sys.argv) > 1:
        # the files have to opened using iso-8859-1-encoding, because the default encoding with utf-8 doesn't work
        text = read_line_by_line()
        current_line = 0
        questions_and_answers = {person_a: list(), person_b: list()}
        # iterates through all lines of the file and checks when a line begins with the abbreviation
        # of one of the interviewpartners provided with the parameters(person_a/person_b) in the script-call. If so,
        # the inner while-loop will loop through the next lines till the end of the current paragraph always ending with
        # #\n was found and then adding the current_paragraph/answer to the list questions_answers
        while current_line < len(text):
            
            # check if the current line starts either with the abbreviation of person_a or person_b
            if text[current_line].startswith(str(person_a)) or text[current_line].startswith(str(person_b)):
                # extract the current key a.k.a. the current person from the beginning of the current line
                current_key = text[current_line][0:2]
                # define the starting line of the current paragraph as the current line
                paragraph_line = current_line
                # declare a new string that will contain the current paragraph as text
                current_paragraph = ""
                # at last the bool end_of_line is define to be triggerd if the end of a line was reached
                end_of_line = False
                # iterate through the lines of text till the end of the current paragraph or the whole text was reached
                while end_of_line is False and paragraph_line < len(text):

                    current_paragraph += text[paragraph_line]
                    # There is his special case when an answer is only one line long
                    # in that case the counter of the current line should not be increased because it would
                    # result in the skipping of the next line
                    if re.search('#\n$', text[paragraph_line]) and text[current_line].startswith(current_key):
                        end_of_line = True

                    else:
                        paragraph_line += 1

                questions_and_answers[current_key].append(current_paragraph)
                current_line = paragraph_line

            current_line += 1

        return questions_and_answers
    
    else:
        print("No textfile found")


# supportive function to split up a paragraph into single sentences
def get_sentences(paragraph):
    # to split up the string the split function is used
    # after that the last element of the list of sentences will be dropped
    # because it only contains the final timestamp
    sentences = paragraph.split('. ')
    return sentences


# utility function using bert to find the keywords from a provided paragraph
def keyword_by_bert(paragraph, numKeywords, n_gram_min, n_gram_max):
    # Based on https://towardsdatascience.com/keyword-extraction-with-bert-724efca412ea
    # import ntlk.corpus.stopwords to have access to german stopwords
    from nltk.corpus import stopwords
    # mport sklearn for the feature extraction
    from sklearn.feature_extraction.text import CountVectorizer
    # sentence_transformer is needed to transform the text and the candidtaes into vectors
    from sentence_transformers import SentenceTransformer
    # import the cosine_similarity, because it can be used to find the between
    # calculate the similarity between candidates and the document
    from sklearn.metrics.pairwise import cosine_similarity
    
    # n_gram_range is used to define the size of the candidates
    # a range from 1,1 means that
    n_gram_range = (n_gram_min, n_gram_max)
    print("n_gram_range set from " + str(n_gram_min) + " to " + str(n_gram_max))
    stop_words = stopwords.words('german')
    # Extract candidate words/phrases
    count = CountVectorizer(ngram_range=n_gram_range, stop_words=stop_words).fit([paragraph])
    # count will contain a list of feature words from the given text stripped of any stopwords
    # to access the extracted features use the get_feature_names_out()-function
    candidates = count.get_feature_names_out()
    print("extracting current candidates: ")
    # print(candidates)
    # define a sentenceTransformer using distilbert
    # distilbert-base-nli-mean-tokens is a pretrained model that will be used for keyword-extraction
    print("Applying the candidate to the sentence transformer")
    model = SentenceTransformer('distilbert-base-nli-mean-tokens')
    # encode the current paragraph using the provided model
    doc_embedding = model.encode([paragraph])
    candidate_embeddings = model.encode(candidates)
    # print("canditate embeddings:")
    # print(candidate_embeddings)
    # now find the keyword using cosine similarity 
    print("Using cosine similarity to find the most fitting candidates:")
    top_n = 5 if numKeywords is None else numKeywords
    if(len(paragraph) <= 5):
        top_n = 1
    
    print("top_n = " + str(top_n) + "\n\n")
    distances = cosine_similarity(doc_embedding, candidate_embeddings)
    keywords = [candidates[index] for index in distances.argsort()[0][-top_n:]]
    print("Most fitting " + str(top_n) + " keywords suggested by bert and sklearn:\n")
    print(keywords)
    
    
# utility function for the extraction of keyphrases with at least one noun
def extract_keyphrases(paragraph):
    # Based on https://towardsdatascience.com/enhancing-keybert-keyword-extraction-results-with-keyphrasevectorizers-3796fa93f4db
    from keyphrase_vectorizers import KeyphraseCountVectorizer
    # import keybert
    from keybert import KeyBERT
    # Import flair, a NLP Framework that's easy to use
    from flair.embeddings import TransformerDocumentEmbeddings
    # Small pythonScripts that prints the text between two lines
    # Init German KeyBERT model
    kw_model = KeyBERT(model=TransformerDocumentEmbeddings('dbmdz/bert-base-german-uncased'))
    # Init vectorizer for the German language using a position pattern including an adjective and a noun 
    # or an adverb and a verb and using german stopwords
    vectorizer = KeyphraseCountVectorizer(spacy_pipeline='de_core_news_sm', pos_pattern='<ADJ.*>*<N.*>+|<ADV.*>*<VERB.*>+', stop_words='german')
    # extracted keyphrases and return them
    keywords = kw_model.extract_keywords(docs=paragraph, vectorizer=vectorizer)
    return keywords;

# utilityfuncton for primitive extractive textsummarization
def summarize(paragraph):
    # Based on https://medium.com/analytics-vidhya/text-summarization-using-bert-gpt2-xlnet-5ee80608e961s
    # Import summarizer and TransformerSummarizer
    from summarizer import Summarizer
    # import every transformer to have access to all pre-trained models
    from transformers import DistilBertTokenizer, DistilBertModel, logging
    # Command that prevents any error or warning logs from being displayed, if they are to distracting
    logging.set_verbosity_error()
    # define a tokenizer
    d_tokenizer = DistilBertTokenizer.from_pretrained('dbmdz/distilbert-base-german-europeana-cased') # 'distilbert-base-multilingual-cased')
    d_model = DistilBertModel.from_pretrained('dbmdz/distilbert-base-german-europeana-cased', output_hidden_states=True)
    # create a summarizer-model that uses multi-language model and tokenizer
    bert_model = Summarizer(custom_model=d_model, custom_tokenizer=d_tokenizer)
    
    bert_summary = ''.join(bert_model(paragraph, min_length=60))
    print("\n\nGenerated summary: ")
    print(bert_summary)
    print("\n\n")
