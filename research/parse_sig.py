from spacy.cli.train import train
import spacy
from word2number import w2n
from dataclasses import dataclass


@dataclass
class StructuredSig():
    drug: str
    form: str
    strength: str
    frequencyType: str
    interval: int
    dosageAmount: int
    periodType: str
    periodAmount: int


def parse_sig(sig):
    sig_preprocessed = convert_words_to_numbers(sig.strip().lower())
    trained = spacy.load('research/example_model/model-last')
    model_output = trained(sig_preprocessed)
    return create_structured_sig(model_output)


def create_structured_sig(model_output):
    dosage, drug, form, freq_type, interval, periodType, periodAmount, strength = None, None, None, None, None, None, None, None
    for entity in model_output.ents:
        text = entity.text
        label = entity.label_
        if label == 'Dosage':
            dosage = text
        if label == 'Drug':
            drug = text
        if label == 'Form':
            form = text
        if label == 'Frequency':
            freq_type = get_frequency_type(text)
            interval = get_interval(text)
        if label == 'Duration':
            periodType = get_frequency_type(text)
            periodAmount = get_interval(text)
        if label == 'Strength':
            strength = text
    return StructuredSig(drug, form, strength, freq_type, interval, dosage, periodType, periodAmount)
 
def is_number_word(word):
    number_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
    return word in number_words

def convert_words_to_numbers(sentence):
    words = sentence.split()
    output_words = []
    for word in words:
        if is_number_word(word):
            output_words.append(str(w2n.word_to_num(word)))
        else:
            output_words.append(word)
    return ' '.join(output_words)

def get_frequency_type(frequency):
    if "day" in frequency:
        return "Day"
    if "week" in frequency:
        return "Week"
    if "month" in frequency:
        return "Month"
    
def get_interval(frequency): 
    for word in frequency.split():
        if is_number_word(word):
            return w2n.word_to_num(word)
    return 1


inp = 'take one tablet of aderol 150mg by mouth every two days for one week'
print(parse_sig(inp))