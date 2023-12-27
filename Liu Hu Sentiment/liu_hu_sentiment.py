import csv
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from preprocess import Preprocess

def load_sentiment_lexicon(filename):
    lexicon = {}
    with open(filename, 'r', encoding='utf-8') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        for row in reader:
            # Here the score is converted to a float
            word = row['Term']
            score = row['Polarity_Avg']
            lexicon[word] = float(score) if score else None  # Using `None` if there is no score

    return lexicon


def load_text_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        # Read the contents of the file
        contents = file.read()

    return contents

def calculate_sentiment_score(words, lexicon):
    pos_score = 0
    neg_score = 0
    maxscore = 0
    for word in words:
        if word in lexicon and lexicon[word]>0:
            pos_score += 1
        elif word in lexicon and lexicon[word]<0:
            neg_score += -1
        maxscore +=1
    return pos_score, neg_score, maxscore

def normalize_sentiment(pscore,nscore,maxscore):
    normalized_score = 100*(pscore-nscore)/maxscore
    return normalized_score

p = Preprocess()

# Load sentiment lexicon
lexicon = load_sentiment_lexicon('my_lexicon.tsv')

# Example text
text = load_text_file('arthro.txt')

words = p.tokenize(text)

# Calculate sentiment score
pscore, nscore, maxscore = calculate_sentiment_score(words, lexicon)

# Classify sentiment as normalized score
sentiment_score = normalize_sentiment(pscore,nscore,maxscore)

# Print the normalized sentiment score
print("Sentiment Score:", sentiment_score)