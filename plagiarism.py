import argparse
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
nltk.download('stopwords')
import nltk
nltk.download('punkt')
# def preprocess(text):
#     """Preprocesses the text by removing non-alphabetic characters, stop words, and stemming the words."""
#     stop_words = set(stopwords.words('english'))
#     stemmer = PorterStemmer()

#     tokens = word_tokenize(text.lower())
#     tokens = [stemmer.stem(token) for token in tokens if token.isalpha() and token not in stop_words]

#     return ' '.join(tokens)

def preprocess(text):
    """Preprocesses the text by removing non-alphabetic characters, stop words, and stemming the words."""
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()

    tokens = word_tokenize(text.lower())
    tokens = [stemmer.stem(token) for token in tokens if token.isalpha() and token not in stop_words]

    if not tokens:  # If the list of tokens is empty
        return ''   # Return an empty string

    return ' '.join(tokens)

def calculate_similarity(text1, text2):
    """Calculates the cosine similarity score between two texts using TF-IDF."""
    texts = [preprocess(text1), preprocess(text2)]
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(texts)

    return cosine_similarity(tfidf)[0][1]

def plag_checker_master(l):
    #print(l)
    try:
        num_files = len(l[0][0])
    except:
        num_files = 0
    
    plag_results = []
    for i in range(num_files):
        
    
        for file_group in l:
            l_file = []
            for file in file_group:
                print(file)
                l_file.append(file[0].decode('utf-8'))
            
            print(l_file)
            l3 = plag_checker(l_file)
                
            plag_results.append(l3)
    #print("^^^^")
    #print(plag_results)
    return plag_results
            
        
def plag_checker(l):
    ll = []
    len_l=len(l)
    for x in range(len_l):
        z=0
        for y in range(len_l):
            
            if(x!=y):
                if(z<calculate_similarity(l[x],l[y])):
                    z=calculate_similarity(l[x],l[y])
        if(z>0.8):
            ll.append(1)
        else:
            ll.append(0)
            
    return ll
