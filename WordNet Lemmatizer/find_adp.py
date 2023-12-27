import re

# Read lexicon words
def read_lexicon(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return set(line.split()[1] for line in file)
    
def read_exceptions(filename):
    exceptions = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()
            if parts and len(parts) == 2:
                exceptions[parts[0]] = parts[1]
    return exceptions

def find_adp_lemma(adp, exceptions):
    # First check if the adjective is an exception
    if adp in exceptions:
        return exceptions[adp]

    return adp  # If no lemma is found, return the original adjective    