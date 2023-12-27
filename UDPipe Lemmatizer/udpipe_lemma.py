import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from ufal.udpipe import Model, Pipeline
from preprocess import Preprocess
from wordcloud_gen import generate_word_cloud, save_word_cloud
import re
import unicodedata

def is_greek_and_not_english(word):
    # Check if the word has only Greek characters and punctuation, excluding English-only words.
    greek_or_punct = lambda char: 'GREEK' in unicodedata.name(char) or not char.isalpha()
    return all(greek_or_punct(char) for char in word)

def parse_conllu(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    word_lemma_pairs = []
    # Allow words with punctuation but no numbers
    word_pattern = re.compile(r"^[^\d_!@#$%&*\'\"-,»«:;/=·-]+$")  # Exclude digits and underscores

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):  # Skip empty lines and comments
            continue
        fields = line.split('\t')
        if len(fields) >= 3:  # Ensure there are enough fields
            word = fields[1]
            lemma = fields[2]
            # Check if the word matches the defined pattern and is Greek excluding English
            if word_pattern.match(word) and is_greek_and_not_english(word):
                word_lemma_pairs.append((word, lemma))
    
    return word_lemma_pairs


# Load the model 
model = Model.load("greek-gdt-ud-2.5-191206.udpipe")
pipeline = Pipeline(model, 'tokenize', Pipeline.DEFAULT, Pipeline.DEFAULT, 'conllu')

def lemmatize_single_word(word, pipeline):
    processed = pipeline.process(word)
    # Extract the lemma of the first word from the processed output
    for line in processed.split('\n'):
        if not line.startswith('#') and line.strip():  # Skip comment lines and empty lines
            parts = line.split('\t')
            if len(parts) > 2:
                lemma = parts[2]
                return lemma
    return word  # Return the original word if no lemma found

p = Preprocess()

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to process text and extract lemmas
def lemmatize_text(input_file_path, stopwords_file, pipeline):
    text = read_text_file(input_file_path)

    # Preprocessing text
    stopwords = p.load_stopwords(stopwords_file)
    text = p.remove_stopwords(text, stopwords)
    text = p.remove_symbols(text)
    words = p.tokenize(text)

    lemmatized_words = []
    for word in words:
        # Lemmatize the word using the custom function with POS tag
        lemma = lemmatize_single_word(word, pipeline)
        lemmatized_words.append(lemma)

        # Joining the stemmed words back into a string
        lemmatized_text = ' '.join(lemmatized_words)

    # Create word cloud
    generate_word_cloud(lemmatized_text)

def test_udpipe_lemmatizer(test_data, pipeline):
    correct_predictions = 0
    total_predictions = 0
    incorrect_predictions = []

    for word, actual_lemma in test_data:
        predicted_lemma = lemmatize_single_word(word, pipeline) # Use UDPipe to get the lemma
        if predicted_lemma == actual_lemma:
            correct_predictions += 1
        else:
            incorrect_predictions.append((word, predicted_lemma, actual_lemma))
        total_predictions += 1

    accuracy = (correct_predictions / len(test_data)) * 100 if total_predictions > 0 else 0
    
    print(f"UDPipe Lemmatization accuracy: {accuracy:.2f}%")

# Parse the test CONLLU files
test_data_file1 = parse_conllu('el_gdt-ud-test.conllu')
test_data_file2 = parse_conllu('el_gud-ud-test.conllu')
test_data = test_data_file1 + test_data_file2

input_file = 'arthro.txt'
stopwords_file = 'stopwords.txt'  
lemmatize_text(input_file, stopwords_file, pipeline)

# Uncomment to evaluate udpipe lemmatizer
#test_udpipe_lemmatizer(test_data, pipeline)

