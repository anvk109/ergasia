import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from greekstemmer import GreekStemmer
from preprocess import Preprocess
from wordcloud_gen import generate_word_cloud, save_word_cloud

p = Preprocess()

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def test_greek_stemmer_on_file(input_file_path,stopwords_file):
    text = read_text_file(input_file_path)

    # Preprocessing text
    stopwords = p.load_stopwords(stopwords_file)
    text = p.remove_stopwords(text, stopwords)
    text = p.remove_symbols(text)
    text = p.remove_accent(text)
    words = p.tokenize(text)

    # Initialize GreekStemmer
    stemmer = GreekStemmer()

    # Applying the stemmer to each word
    stemmed_words = [stemmer.stem(word) for word in words]

    # Joining the stemmed words back into a string
    stemmed_text = ' '.join(stemmed_words)

    # Create word cloud
    generate_word_cloud(stemmed_text)

# Example 
input_file = 'arthro.txt'
stopwords_file = 'stopwords.txt'  
test_greek_stemmer_on_file(input_file,stopwords_file)