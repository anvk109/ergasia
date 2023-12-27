from ufal.udpipe import Model, Pipeline

class UDPipeModel:
    def __init__(self, model_path):
        self.model = Model.load(model_path)
        if not self.model:
            raise Exception("Cannot load UDPipe model from file '%s'" % model_path)
        self.pipeline = Pipeline(self.model, "tokenize", Pipeline.DEFAULT, Pipeline.DEFAULT, "conllu")

    def tokenize_tag(self, text):
        processed = self.pipeline.process(text)
        return [(word[1], word[3]) for sentence in self._parse_conllu(processed) for word in sentence]

    @staticmethod
    def _parse_conllu(input_str):
        sentences = []
        sentence = []
        for line in input_str.split('\n'):
            line = line.strip()
            if line:
                if line.startswith('#'):
                    continue
                row = line.split('\t')
                if len(row) != 10:
                    raise Exception("Unexpected number of columns in the CONLL-U format.")
                sentence.append(row)
            else:
                if len(sentence) > 0:
                    sentences.append(sentence)
                    sentence = []
        if len(sentence) > 0:
            sentences.append(sentence)
        return sentences

if __name__ == "__main__":
    udpipe_model_path = "greek-gdt-ud-2.5-191206.udpipe"
    model = UDPipeModel(udpipe_model_path)

    greek_words = [
    "καλός", "μεγάλος", "μικρός", "όμορφος", "άσχημος", "νέος", "παλιός", "σωστός", "λάθος", "γρήγορος",
    "αργός", "δυνατός", "αδύνατος", "έξυπνος", "χαζός", "ζεστός", "κρύος", "καθαρός", "βρώμικος", "ψηλός",
    "χαμηλός", "βαθύς", "ρηχός", "σκληρός", "μαλακός", "ευχάριστος", "δυσάρεστος", "ελαφρύς", "βαρύς", "σκοτεινός",
    "φωτεινός", "κοντός", "μακρύς", "στενός", "φαρδύς", "πλούσιος", "φτωχός", "γεμάτος", "άδειος", "σκέτος",
    "πικάντικος", "γλυκός", "αλμυρός", "οξύς", "βαρετός", "ενδιαφέρων", "πεινασμένος", "κορεσμένος", "κουρασμένος", "ξεκούραστος",
    "υγρός", "ξηρός", "δημοφιλής", "άγνωστος", "φρέσκος", "σάπιος", "νωπός", "στεγνός", "ακριβός", "φθηνός",
    "κενός", "γεμάτος", "βροχερός", "ηλιόλουστος", "υποχρεωτικός", "προαιρετικός", "κομψός", "ατίθασος", "χοντρός", "λεπτός",
    "μοναχικός", "κοινωνικός", "κακός", "καλόκαρδος", "απλός", "πολύπλοκος", "ήσυχος", "θορυβώδης", "σαφής", "ασαφής",
    "ενεργητικός", "παθητικός", "ανοιχτός", "κλειστός", "αντιφατικός", "αρμονικός", "δραστήριος", "χαλαρός", "σταθερός", "ασταθής",
    "ακατέργαστος", "επεξεργασμένος", "διακριτικός", "φανερός", "μετριοπαθής", "έντονος", "υπερήφανος", "ταπεινός", "συντηρητικός", "προοδευτικός"
]
    correct_tags = ["ADJ"] * len(greek_words)  
    
    text = " ".join(greek_words)
    tagged_words = model.tokenize_tag(text)

    correct_count = 0
    for (word, pos), correct_tag in zip(tagged_words, correct_tags):
        if pos == correct_tag:
            correct_count += 1
        print(f"{word} - {pos}")

    print(f"\nCorrectly tagged: {correct_count}/{len(greek_words)}")


