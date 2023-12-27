import re

def read_lexicon(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return set(line.split()[1] for line in file)

def read_suffixes(filename):
    suffixes = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split('\t')
            if parts and len(parts) > 1:
                suffixes[parts[0]] = parts[1:]
    return suffixes

def move_tone_to_previous_vowel(word):
    vowels = "αεηιοωυ"
    accented_vowels = "άέήίόώύ"
    accent_map = dict(zip(accented_vowels, vowels))

    chars = list(word)
    for i, char in enumerate(chars):
        if char in accented_vowels and i > 0:
            for j in range(i - 1, -1, -1):
                if chars[j] in vowels:
                    chars[j] = accented_vowels[vowels.index(chars[j])]
                    chars[i] = accent_map[char]
                    break
    return ''.join(chars)

# Load exception rules for nouns
def read_exceptions(filename):
    exceptions = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()
            if parts and len(parts) == 2:
                exceptions[parts[0]] = parts[1]
    return exceptions

def find_noun_lemma(noun, lexicon, suffixes, exceptions):
    if noun in exceptions:
        return exceptions[noun]

    for suffix, replacements in suffixes.items():
        if noun.endswith(suffix):
            noun_base = noun[:-len(suffix)]
            for replacement in replacements:
                candidates = [noun_base + replacement, 
                              move_tone_to_previous_vowel(noun_base + replacement)]
                for candidate in candidates:
                    if candidate in lexicon:
                        return candidate
    return noun  # Return the noun itself if no lemma is found

# Example usage
#lexicon = read_lexicon('GreekLex_LowerCase.txt')
#suffixes = read_suffixes('noun.txt')
#nouns = ['παιδιά', 'πόλης', 'γυναικών', 'κήπους', 'δασκάλου', 'σκύλος', 'μαθητής', 'νησί', 'παραθύρων', 'αγάπης']  # Replace with your list of nouns
#lemmas = [find_noun_lemma(noun, lexicon, suffixes)for noun in nouns]
#print(lemmas)




