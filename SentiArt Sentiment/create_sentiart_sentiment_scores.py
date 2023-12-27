import pandas as pd
import numpy as np
from scipy import spatial

# Function to compute cosine similarity
def compute_cosine_similarity(vector_a, vector_b):
    return 1 - spatial.distance.cosine(vector_a, vector_b)

# Extract vectors for a given list of words from the .vec file
def load_vectors_from_vec_file(vec_file_path):
    vectors = {}
    with open(vec_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            word, *vector = line.strip().split()
            vectors[word] = np.array([float(i) for i in vector])
    return vectors

# Load text data
txt_file = 'SUBTLEX-GR_restricted.txt'
txt_df = pd.read_csv(txt_file, sep='\t', encoding='utf-8')
word_list = txt_df["Word"].tolist()

# List of emotions and labels
emotions = ['θυμός', 'φόβος', 'απέχθεια', 'ευτυχία', 'λύπη', 'έκπληξη']
positive_labels = ['ευχαρίστηση', 'ευτυχία', 'απόλαυση', 'υπερηφάνεια', 'ανακούφιση', 'ικανοποίηση', 'έκπληξη']
negative_labels = ['απέχθεια', 'αμηχανία', 'φόβος', 'λύπη', 'ντροπή']

# Load all vectors from the .vec file
vectors = load_vectors_from_vec_file('cc.el.300.vec')

# Process and compute similarity scores and valence
results = []
for word in word_list:
    if word in vectors:
        word_vector = vectors[word]
        
        avg_pos_sim = np.mean([compute_cosine_similarity(word_vector, vectors[pos_label]) for pos_label in positive_labels if pos_label in vectors])
        avg_neg_sim = np.mean([compute_cosine_similarity(word_vector, vectors[neg_label]) for neg_label in negative_labels if neg_label in vectors])
        valence = avg_pos_sim - avg_neg_sim
        
        emotion_scores = {emotion: compute_cosine_similarity(word_vector, vectors.get(emotion, np.zeros_like(word_vector))) for emotion in emotions}
        
        results.append((word, valence, emotion_scores['θυμός'], emotion_scores['φόβος'], emotion_scores['απέχθεια'], emotion_scores['ευτυχία'], emotion_scores['λύπη'], emotion_scores['έκπληξη']))

# Save results
results_df = pd.DataFrame(results, columns=['Word', 'Valence', 'Anger', 'Fear', 'Disgust', 'Happiness', 'Sadness', 'Surprise'])
results_df.to_excel('sentiment_valence_results.xlsx', index=False)


