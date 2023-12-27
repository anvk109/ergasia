import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from Learn_Lemmagen_RDR import create_rdr_tree, parse_conllu
from preprocess import Preprocess
from wordcloud_gen import generate_word_cloud, save_word_cloud

# Use the function to get the entire RDR tree
entire_rdr = create_rdr_tree()

def Transform(wordform, transformation):
    # This function needs to apply the transformation string to the wordform
    # Transformation string format: '"suffix"->"replacement"'
    old, new = transformation.replace('"', '').split('-->')
    if wordform.endswith(old):
        return wordform[:len(wordform)-len(old)] + new
    else:
        return wordform  # Return wordform unchanged if suffix does not match

def lemmatize_word(word, rdr_node):
    if rdr_node is None:
        return word

    if word.endswith(rdr_node.condition):
        transformation = rdr_node._class.split('"-->"')
        suffix1 = transformation[0].strip('"')
        suffix2 = transformation[1].strip('"') if len(transformation) > 1 else ''

        if suffix1 == "":  # If the suffix to be removed is empty
            lemma = word + suffix2  # Add the new suffix directly
        else:
            if word.endswith(suffix1):
                lemma = word[:-len(suffix1)] + suffix2
            else:
                lemma = word

        for exception in rdr_node.exceptions:
            if word.endswith(exception.condition):
                lemma = lemmatize_word(word, exception)
                break

        return lemma

    return lemmatize_word(word, next(iter(rdr_node.exceptions), None)) 

def test_lemmatizer(test_data, rdr_tree):
    correct_predictions = 0
    incorrect_predictions = []

    for word, actual_lemma in test_data:
        predicted_lemma = lemmatize_word(word, rdr_tree)
        if predicted_lemma == actual_lemma:
            correct_predictions += 1
        else:
            incorrect_predictions.append((word, predicted_lemma, actual_lemma))

    accuracy = (correct_predictions / len(test_data)) * 100

    return accuracy

p = Preprocess()

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to process text and extract lemmas
def lemmatize_text(input_file_path, stopwords_file,rdr_tree):
    text = read_text_file(input_file_path)

    # Preprocessing text
    stopwords = p.load_stopwords(stopwords_file)
    text = p.remove_stopwords(text, stopwords)
    text = p.remove_symbols(text)
    words = p.tokenize(text)

    lemmatized_words = []
    for word in words:
        # Lemmatize the word using the custom function with POS tag
        lemma = lemmatize_word(word,rdr_tree)
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
lemmatize_text(input_file, stopwords_file, entire_rdr)

# Test the lemmatizer - Uncomment to see evaluation
#accuracy = test_lemmatizer(test_data, entire_rdr)
#print(f"Lemmatization accuracy: {accuracy:.2f}%")


