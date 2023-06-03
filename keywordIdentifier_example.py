# This script should help to identify keywords in the interviews using rake_nltk
# import sys
# import util
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
from requests_html import HTMLSession
from rake_nltk import Rake


def extract_text():
    s = HTMLSession()
    url = 'https://towardsdatascience.com/keyword-extraction-process-in-python-with-natural-language-processing-nlp-d769a9069d5c'
    response = s.get(url)
    return response.html.find('section', first=True).text


r = Rake()
r.extract_keywords_from_text(extract_text())
print(r.get_ranked_phrases_with_scores())
