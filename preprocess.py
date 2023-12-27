import re
import unicodedata as ud

class Preprocess:

    ###---- Tranformation ---###
    def remove_accent(self, text):
        text = re.sub(r'ϊ|ΐ','ι', text)
        text = re.sub(r'ϋ|ΰ','υ', text)
        text = re.sub(r'Ϊ','Ι', text)
        text = re.sub(r'Ϋ','Υ', text)

        d = {ord('\N{COMBINING ACUTE ACCENT}'):None}

        text = ud.normalize('NFD',text).translate(d)

        return text

    def lowercase(self, text):
        text = text.lower()
        return text

    def uppercase(self, text):
        text = text.upper()
        return text



    ###---- Filtering ---###
    def load_stopwords(self,filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            stopwords = file.read().splitlines()
        return stopwords

    def remove_digits(self,text):
        text = re.sub(r'\d+','', text)
        return text
    
    def remove_symbols(self,text):
        text = re.sub(r'[.,@#%^*:{};!?»«()|\'"‘’“”…\-–—$&><\/\[\]]', '', text)
        return text
    
    def remove_stopwords(self, text, stopwords):
        pattern = r'\b(?:' + '|'.join(map(re.escape, stopwords)) + r')\b'
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        return text


    ###---- Tokenization ---###
    def tokenize(self, text):
        words = text.split()
        return words

    