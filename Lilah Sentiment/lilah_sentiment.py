import pandas as pd

# Load the NRC Emotion Lexicon for Greek words
def load_lexicon(filename):
    lexicon = pd.read_csv(filename, sep='\t')
    lexicon.set_index('Greek Word', inplace=True)
    return lexicon

# Analyze a given text based on the lexicon
def analyze_text(text, lexicon):
    words = text.split()
    
    # Filter alphabetic words
    alphabetic_words = [word for word in words if word.isalpha()]
    num_alphabetic_words = len(alphabetic_words)
    
    # Check which words are in the lexicon
    words_in_lexicon = [word for word in alphabetic_words if word in lexicon.index]
    num_words_in_lexicon = len(words_in_lexicon)
    
    # Compute average sentiment/emotion value for words in lexicon
    emotions = ['positive', 'negative', 'anger', 'anticipation', 'disgust', 'fear', 'joy', 'sadness', 'surprise', 'trust']
    avg_emotion_values = {}
    for emotion in emotions:
        avg_emotion_values[emotion] = lexicon.loc[words_in_lexicon][emotion].mean()
    
    return num_alphabetic_words, num_words_in_lexicon, avg_emotion_values

if __name__ == '__main__':
    # Load the lexicon and the text file
    text_file = "arthro.txt"
    lexicon = load_lexicon("Greek-NRC-EmoLex.txt")  
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read().lower()  # Convert to lowercase for matching

    # Analyze the text
    num_alpha, num_in_lexicon, avg_emotions = analyze_text(text, lexicon)
    
    # Print the results
    print(f"Total number of alphabetic words in the text: {num_alpha}")
    print(f"Number of words from the text that are present in the lexicon: {num_in_lexicon}")
    print("Average sentiment/emotion values:")
    for emotion, value in avg_emotions.items():
        print(f"{emotion}: {value}")



