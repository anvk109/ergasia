import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
import stanza
import unicodedata
import re
import find_verb as fv
import find_noun as fn
import find_adj as fa
import find_adp as fadp
from preprocess import Preprocess
from wordcloud_gen import generate_word_cloud, save_word_cloud



# Load custom lexicon and rules
lexicon = fv.load_lexicon('GreekLex_LowerCase.txt')
verb_exceptions = fv.load_exceptions('verbs_exc.txt')
verb_suffix_changes = fv.load_suffix_changes('verbs.txt')
noun_suffix_changes = fn.read_suffixes('noun.txt')
noun_exceptions = fn.read_exceptions('noun_exc.txt')
adj_suffix_changes = fa.read_suffixes('adj.txt')  
adj_exceptions = fa.read_exceptions('adj_exc.txt')
adp_exceptions = fadp.read_exceptions('adp_exc.txt')
pron_changes = fa.read_suffixes

# Suppress Stanza Logging
import logging
logging.getLogger('stanza').setLevel(logging.CRITICAL)

# Initialize Stanza pipeline for Greek
stanza_nlp = stanza.Pipeline(lang='el', processors='tokenize,pos', download_method=None, logging_level='ERROR')

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

def lemmatize_single_word_custom(word, pos_tag):
    if pos_tag not in ['PROPN']:
        word = word.lower()
    if pos_tag in ['AUX', 'VERB']:
        return fv.find_verb_lemma(word, lexicon, verb_exceptions, verb_suffix_changes)
    elif pos_tag in ['NOUN', 'PROPN']:
        return fn.find_noun_lemma(word, lexicon, noun_suffix_changes, noun_exceptions)
    elif pos_tag in ['ADJ', 'DET','PRON','NUM']:
        return fa.find_adjective_lemma(word, lexicon, adj_suffix_changes, adj_exceptions)
    elif pos_tag in ['ADP']:
        return fadp.find_adp_lemma(word, adp_exceptions)
    return word

def eval_wordnet_lemmatizer_with_pos(test_data, stanza_nlp):
    correct_predictions = 0
    total_predictions = len(test_data)
    incorrect_predictions = []

    for word, actual_lemma in test_data:
        # Process the word using Stanza to get the POS tag
        doc = stanza_nlp(word)
        pos_tag = doc.sentences[0].words[0].pos if doc.sentences else 'X'  # 'X' for unknown

        # Lemmatize the word using the custom function with POS tag
        predicted_lemma = lemmatize_single_word_custom(word, pos_tag)

        if predicted_lemma == actual_lemma:
            correct_predictions += 1
        else:
            incorrect_predictions.append((word, predicted_lemma, actual_lemma, pos_tag))

    accuracy = (correct_predictions / total_predictions) * 100 if total_predictions > 0 else 0
    
    print(f"WordNet Lemmatization with POS accuracy: {accuracy:.2f}%")

p = Preprocess()

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def test_wordnet_lemmatizer_on_file(input_file_path,stopwords_file):
    text = read_text_file(input_file_path)

    # Preprocessing text
    stopwords = p.load_stopwords(stopwords_file)
    text = p.remove_stopwords(text, stopwords)
    text = p.remove_symbols(text)
    words = p.tokenize(text)

    lemmatized_words = []
    for word in words:
        # Process the word using Stanza to get the POS tag
        doc = stanza_nlp(word)
        pos_tag = doc.sentences[0].words[0].pos if doc.sentences else 'X'  # 'X' for unknown

        # Lemmatize the word using the custom function with POS tag
        lemma = lemmatize_single_word_custom(word, pos_tag)
        lemmatized_words.append(lemma)

        # Joining the stemmed words back into a string
        lemmatized_text = ' '.join(lemmatized_words)
        

    # Create word cloud
    generate_word_cloud(lemmatized_text)

        
# Parse the test CONLLU files
test_data_file1 = parse_conllu('el_gdt-ud-test.conllu')
test_data_file2 = parse_conllu('el_gud-ud-test.conllu')

# Combine the data from both files
test_data = test_data_file1 + test_data_file2

input_file = 'arthro.txt'
stopwords_file = 'stopwords.txt'  
test_wordnet_lemmatizer_on_file(input_file,stopwords_file)

#Uncomment to test evaluation
#eval_wordnet_lemmatizer_with_pos(test_data, stanza_nlp)
