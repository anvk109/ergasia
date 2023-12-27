import re

def load_lexicon(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return {line.strip().split('\t')[1] for line in file if '\t' in line}
    except IOError as e:
        print(f"Error loading lexicon file: {e}")
        return set()

def load_exceptions(filename):
    exceptions = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()
            if parts and len(parts) == 2:
                exceptions[parts[0]] = parts[1]
    return exceptions

def load_suffix_changes(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            changes = {}
            for line in file:
                parts = line.strip().split('\t')
                if len(parts) > 1:
                    changes[parts[0]] = parts[1:]
            return changes
    except IOError as e:
        print(f"Error loading suffix changes file: {e}")
        return {}

accents_translation_table = str.maketrans('άέήίόύώ', 'αεηιουω')

def remove_accents(verb):
    return verb.translate(accents_translation_table)

def replace_ending(verb, ending, new_endings, lexicon):
    verb_without_tone = remove_accents(verb[:-len(ending)])
    for new_ending in new_endings:
        new_verb = verb_without_tone + new_ending
        if new_verb in lexicon:
            return new_verb
    return None

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

def move_tone_to_next_vowel(word):
    vowels = "αεηιοωυ"
    accented_vowels = "άέήίόώύ"
    accent_map = dict(zip(accented_vowels, vowels))

    chars = list(word)
    for i, char in enumerate(chars):
        if char in accented_vowels:
            for j in range(i + 1, len(chars)):  # Check following chars
                if chars[j] in vowels:
                    chars[j] = accented_vowels[vowels.index(chars[j])]  # Add accent
                    chars[i] = accent_map[char]  # Remove current accent
                    return ''.join(chars)
            break  # Exit loop if no next vowel is found

    return ''.join(chars) 

def adjust_verb(verb, lexicon):
    suffixes = ['να', 'νες', 'νε', 'ναμε', 'νατε', 'ναν', 'νανε', 'σα', 'σες', 'σε', 'σαμε', 'σατε',  'σαν', 'σανε', 'λα', 'λες', 'λε', 'λαμε', 'λατε',  'λαν', 'λανε',
                'ξα', 'ξες', 'ξε', 'ξαμε', 'ξατε',  'ξαν', 'ξανε', 'φα', 'φες', 'φε', 'φαμε', 'φατε',  'φαν', 'φανε', 'ψα', 'ψες', 'ψε', 'ψαμε', 'ψατε',  'ψαν', 'ψανε',
                'γα', 'γες', 'γε', 'γαμε', 'γατε',  'γαν', 'γανε', 'ζα', 'ζες', 'ζε', 'ζαμε', 'ζατε',  'ζαν', 'ζανε', 'ρα', 'ρες', 'ρε', 'ραμε', 'ρατε',  'ραν', 'ρανε',
                'χα', 'χες', 'χε', 'χαμε', 'χατε',  'χαν', 'χανε']
    re_endings_to_replace = re.compile(r'(αγα|αγες|αγε|αγαμε|αγατε|αγανε|αγαν|ησα|ησες|ησε|ησαμε|ησατε|ησανε|ησαν|θω|θεις|θει|θούμε|θετε|θουν|θουνε)$')
    # Greek vowel mapping from unaccented to accented
    vowels = {'α': 'ά', 'ε': 'έ', 'η': 'ή', 'ι': 'ί', 'ο': 'ό', 'υ': 'ύ', 'ω': 'ώ'}
    
    match = re_endings_to_replace.search(verb)
    if match:
        ending = match.group()
        return replace_ending(verb, ending, ['ώ', 'άω', 'θαίνω'], lexicon) or verb
    
    if any(verb.endswith(suffix) for suffix in suffixes):
        # Replace the suffix to form the correct verb form
        for suffix in suffixes:
            if verb.endswith(suffix):
                verb_without_suffix = verb[:-len(suffix)]
                
                for replacement in ['νω', 'χω', 'φω', 'ζω', 'ω', 'βω', 'χνω', 'αίνω', 'χαίνω', 'νομαι']:
                    new_verb = verb_without_suffix + replacement
                    if new_verb in lexicon:
                        return new_verb
                    new_verb_2 = move_tone_to_next_vowel(new_verb)
                    if new_verb_2 in lexicon:
                        return new_verb_2
                    new_verb_3 = move_tone_to_next_vowel(new_verb_2)
                    if new_verb_3 in lexicon:
                        return new_verb_3
                break    
    if (verb.startswith('έ') or verb.startswith('ή'))and any(verb.endswith(suffix) for suffix in suffixes):
        # Remove 'έ' from the start
        new_verb = verb[1:]
        # Replace the first vowel with its accented version
        for i, char in enumerate(new_verb):
            if char in vowels:
                new_verb = new_verb[:i] + vowels[char] + new_verb[i+1:]
                break

        # Replace the suffix to form the correct verb form
        for suffix in suffixes:
            if new_verb.endswith(suffix):
                #print(suffix)
                verb_without_suffix = new_verb[:-len(suffix)]
                #print(verb_without_suffix)
                
                for replacement in ['νω', 'χω', 'φω', 'ζω', 'ω', 'βω', 'χνω', 'ρνω', 'ρω', 'νομαι']:
                    new_verb = verb_without_suffix + replacement
                    
                    if new_verb in lexicon:
                        return new_verb
                    new_verb = move_tone_to_next_vowel(new_verb)
                    if new_verb in lexicon:
                        return new_verb
                break
                
    return verb  # If no replacement was made

def find_verb_lemma(verb, lexicon, exceptions, suffix_changes):
   # print(f"Processing verb: {verb}")
    if verb in exceptions:
        #print(f"Found in exceptions, returning: {exceptions[verb]}")
        return exceptions[verb]
    
    endings = ['ω', 'ομαι', 'ώ', 'ιέμαι', 'ούμαι', 'άμαι']
    if any(verb.endswith(end) for end in endings) and verb in lexicon:
        return verb

    for suffix, changes in suffix_changes.items():
        #print(f"Checking suffix: {suffix} for verb: {verb}")
        if verb.endswith(suffix):
            #print(f"Matching suffix: {suffix}")
            for change in changes:
                new_verb = verb[:-len(suffix)] + change
                #print(f"Trying change '{change}': {new_verb}")
                if new_verb in lexicon:
                    #print(f"Found in lexicon, returning: {new_verb}")
                    return new_verb
    #print(f"No match found, defaulting to original verb: {verb}")            
    return adjust_verb(verb, lexicon)

