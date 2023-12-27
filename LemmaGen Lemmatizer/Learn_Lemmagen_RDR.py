import re
import json
import unicodedata

class RDR:
    def __init__(self):
        self.condition = ""
        self._class = ""
        self.exceptions = []

    def add_exception(self, exception_rdr):
        #Adds an RDR object to the exceptions list.
        if isinstance(exception_rdr, RDR):
            self.exceptions.append(exception_rdr)
        else:
            raise ValueError("Only RDR objects can be added as an exception.")

    def to_dict(self):
        return {
            "condition": self.condition,
            "_class": self._class,
            "exceptions": [e.to_dict() for e in self.exceptions]
        }

def Sort(examples, method='reverse dictionary sort'):
    # Implementing reverse dictionary sort
    return sorted(examples, key=lambda x: x[0][::-1])

def MostFreqClass(examples, common_suffix):
    #This function determines the most frequent class for a given list of examples,
    #ignoring transformations where the word_suffix is longer than the commonSuffix.
    
    transformations = {}
    for example in examples:
        wordform = example[0]
        lemma = example[1]

        # Calculate the transformation to get from wordform to lemma
        transformation = determine_transformation(wordform, lemma)
        word_suffix = transformation.split('"-->')[0].strip('"')

        # Skip transformations where the word_suffix is longer than the commonSuffix
        if len(word_suffix) > len(common_suffix):
            continue

        if transformation not in transformations:
            transformations[transformation] = 0
        transformations[transformation] += 1

    # If no transformations meet the criteria, return an empty transformation
    if not transformations:
        return '""-->""'
    
    # Return the most frequent transformation that meets the criteria
    return max(transformations, key=transformations.get)

def determine_transformation(word, lemma):
    if word == lemma:
        return '""-->""'

    # Find the first position where the two strings differ
    for i in range(min(len(word), len(lemma))):
        if word[i] != lemma[i]:
            break
    else:
        i = min(len(word), len(lemma))

    # Find the suffixes of the word and lemma starting from the differing position
    word_suffix = word[i:]
    lemma_suffix = lemma[i:]

    return f'"{word_suffix}"-->"{lemma_suffix}"'

def EqualSuffix(word1, word2):
    # Returns the common suffix between 2 words
    # Reverse the words for easier comparison from the back
    reversed_word1 = word1[::-1]
    reversed_word2 = word2[::-1]

    suffix = []

    # Determine the length of the shorter word
    min_length = min(len(word1), len(word2))

    # Compare characters of the reversed words
    for i in range(min_length):
        if reversed_word1[i] == reversed_word2[i]:
            suffix.append(reversed_word1[i])
        else:
            break

    # Return the reversed suffix to get it in the correct order
    return ''.join(suffix[::-1])

def StringLength(s):
    return len(s)

def GetChar(word, position):
    if 0 <= position < len(word):
        return word[position]
    return None

def LearnRecursive(currentExamplesList):
    commonSuffix = EqualSuffix(currentExamplesList[0][0], currentExamplesList[-1][0])
    lengthCommonSuffix = StringLength(commonSuffix)
    
    currentRule = RDR()
    currentRule.condition = commonSuffix
    currentRule._class = MostFreqClass(currentExamplesList, commonSuffix)
    
    start = 0
    i = 0

    while i < len(currentExamplesList) - 1:
        wf1 = currentExamplesList[i][0]
        wf2 = currentExamplesList[i+1][0]

        commonSuffix = EqualSuffix(wf1, wf2)
        charPosition1 = StringLength(wf1) - lengthCommonSuffix - 1
        charPosition2 = StringLength(wf2) - lengthCommonSuffix - 1
        
        if GetChar(wf1, charPosition1) == GetChar(wf2, charPosition2):
            i += 1
            continue
        else:
            exception_examples = currentExamplesList[start:i+1]
            exceptionRule = LearnRecursive(exception_examples)
            exception_transformation = MostFreqClass(exception_examples, commonSuffix)

            # Only add exception if its condition is different from the current rule's condition
            if exceptionRule.condition != currentRule.condition:
                currentRule.add_exception(exceptionRule)

        start = i + 1
        i += 1

    return currentRule


def rdr_to_string(rdr, indent=0):
    # Convert the RDR object into a readable string format
    # Start with the current rule
    result = '\t' * indent + f"RULE: i\"{rdr.condition}\" t{rdr._class}\n"

    # If there are exceptions, recursively handle them
    if rdr.exceptions:
        result += "{:\n"
        for exception in rdr.exceptions:
            result += rdr_to_string(exception, indent+1)
        result += '\t' * indent + ":}\n"

    return result

def LearnRDR(examplesList):
    sortedExamplesList = Sort(examplesList)
    entireRDR = LearnRecursive(sortedExamplesList)
    return entireRDR

def save_rules_to_json(rules, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(rules, json_file, ensure_ascii=False, indent=4)

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



def print_rdr_tree(rdr, indent=0):
    print('\t' * indent + f"RULE: i\"{rdr.condition}\" t{rdr._class}")
    for exception in rdr.exceptions:
        print_rdr_tree(exception, indent + 1)


def create_rdr_tree():
    word_lemma_pairs_file1 = parse_conllu('el_gdt-ud-train.conllu')
    word_lemma_pairs_file2 = parse_conllu('el_gud-ud-train.conllu')

    train_data = word_lemma_pairs_file1 + word_lemma_pairs_file2

    sorted_data = Sort(train_data)
    entire_rdr = LearnRDR(sorted_data)

    return entire_rdr

rdr_tree = create_rdr_tree()

if __name__ == "__main__":
    # If the script is run directly, then create the RDR tree and write it to a file
    rdr_tree = create_rdr_tree()
    with open("results1.txt", "w", encoding="utf-8") as txt_file:
        txt_file.write(rdr_to_string(rdr_tree))