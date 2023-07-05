from krovetzstemmer import Stemmer as BaseStemmer

# Specific stemming definitions we want to use instead of language stemming
stemmer_overrides = {"drops": "drop"}
"""
Represents an english-language stemmer for terms used in doctors' signature.
"""
class SigTermsStemmer():
    def __init__(self):
        self._baseStemmer = BaseStemmer()
    def stem(self, text):
        termFromOverride = stemmer_overrides.get(text)
        if termFromOverride is None:
            return self._baseStemmer.stem(text)
        else:
            return termFromOverride