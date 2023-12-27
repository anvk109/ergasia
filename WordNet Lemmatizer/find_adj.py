import re

# Read lexicon words
def read_lexicon(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return set(line.split()[1] for line in file)

# Load suffix rules
def read_suffixes(filename):
    suffixes = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            if parts and len(parts) > 1:
                suffixes[parts[0]] = parts[1:]
    return suffixes

# Function to try to move the accent to the previous vowel
def move_tone_to_previous_vowel(word):
    vowels = "αεηιοωυ"
    accented_vowels = "άέήίόώύ"
    accent_map = dict(zip(accented_vowels, vowels))

    chars = list(word)
    for i, char in enumerate(chars):
        if char in accented_vowels and i > 0:
            for j in range(i - 1, -1, -1):  # Check previous chars
                if chars[j] in vowels:
                    chars[j] = accented_vowels[vowels.index(chars[j])]  # Add accent
                    chars[i] = accent_map[char]  # Remove current accent
                    break
    return ''.join(chars)

# Load exception rules for adjectives
def read_exceptions(filename):
    exceptions = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()
            if parts and len(parts) == 2:
                exceptions[parts[0]] = parts[1]
    return exceptions

def find_adjective_lemma(adj, lexicon, suffixes, exceptions):
    # First check if the adjective is an exception
    if adj in exceptions:
        return exceptions[adj]
    
    for suffix, replacements in suffixes.items():
        if adj.endswith(suffix):
            # First try without moving the accent
            for replacement in replacements:
                candidate = adj[:-len(suffix)] + replacement
                if candidate in lexicon:
                    return candidate
                candidate_with_moved_accent = move_tone_to_previous_vowel(candidate)
                if candidate_with_moved_accent in lexicon:
                    return candidate_with_moved_accent

    return adj  # If no lemma is found, return the original adjective

        

    

# Example usage
#lexicon = read_lexicon('GreekLex_LowerCase.txt')
#suffixes = read_suffixes('adj.txt')
#exceptions = read_exceptions('adj_exc.txt')
#adjectives = ['πολλούς', 'μεγάλων', 'καλούς', 'γρήγορες', 'πολλού']  # Replace with your list of adjectives
#find_adjective_lemmas(adjectives, lexicon, suffixes, exceptions)