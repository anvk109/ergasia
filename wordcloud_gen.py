from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

def generate_word_cloud(text, max_words=100):
    # Count the words in the text and get the most common
    word_freq = Counter(text.split()).most_common(max_words)
    
    # Convert the list of tuples into a dictionary
    word_freq_dict = dict(word_freq)
    
    # Generate the word cloud using frequencies
    wordcloud = WordCloud(width=800, height=800, max_words=max_words, background_color='white').generate_from_frequencies(word_freq_dict)
    
    # Display the generated image:
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
# Save the word cloud image to a file if needed
def save_word_cloud(wordcloud, filename):
    wordcloud.to_file(filename)