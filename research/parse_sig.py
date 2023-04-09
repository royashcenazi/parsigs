from spacy.cli.train import train
import spacy
from word2number import w2n
from dataclasses import dataclass
import re

# TODO handle multiple instructions in one sentence

"""
Represents a structured medication dosage instructions.
Attributes:
-----------
drug : str
    The name of the medication drug.
form : str
     The form of the medication (e.g. tablet, capsule, injection, etc.).
strength : str
    The strength of the medication (e.g. 10mg, 20mg, etc.).
frequencyType : str
    The type of frequency for the dosage (e.g. daily, weekly, monthly, etc.).
interval : int
     The interval between dosages (e.g. every 4 hours, every 12 hours, etc.).
singleDosageAmount : int
    The amount of the medication in a single dosage (e.g. 1 tablet, 2 capsules, etc.).
periodType : str
    The type of period for the dosage (e.g. days, weeks, months, etc.).
periodAmount : int
    The duration of the period for the dosage (e.g. 7 days, 14 days, etc.).
"""


@dataclass
class StructuredSig():
    drug: str
    form: str
    strength: str
    frequencyType: str
    interval: int
    singleDosageAmount: int
    periodType: str
    periodAmount: int


def parse_sig(sig):
    sig_preprocessed = pre_process(sig)
    sig_preprocessed = re.sub(r'\s+', ' ', sig_preprocessed)
    trained = spacy.load('research/example_model2/model-best')
    model_output = trained(sig_preprocessed)

    # DEBUG
    print([(e, e.label_) for e in model_output.ents])

    return create_structured_sig(model_output, sig_preprocessed)


def pre_process(sig):
    sig = sig.lower().replace('twice', '2 times').replace("once", '1 time')

    sig = add_space_around_parentheses(sig)

    output_words = []
    words = sig.split()
    for word in words:
        if word == 'tab':
            output_words = word.replace('tab', 'tablet')
        else:
            output_words.append(word)
    sig = ' '.join(output_words)

    sig = convert_words_to_numbers(sig)
    return convert_fract_to_num(sig)

def add_space_around_parentheses(s):
    # Add a space before an opening parenthesis if not already separated by a space
    s = re.sub(r'(?<!\s)\(', r' (', s)
    # Add a space after a closing parenthesis if not already separated by a space
    s = re.sub(r'\)(?!\s)', r') ', s)
    return s


def create_structured_sig(model_output, sig_preprocessed):
    duration_string = get_duration_string(sig_preprocessed)
    # The initial values using helper methods are only when them model does not detect the entity (otherwise the detected entity is used)
    dosage, drug, form, freq_type, interval, periodType, periodAmount, strength = get_single_dose(sig_preprocessed), None, None, None, None, get_frequency_type(duration_string), get_interval(duration_string), None
    for entity in model_output.ents:
        text = entity.text
        label = entity.label_
        if label == 'Dosage' and text.split()[0].isnumeric():
            dosage = text.split()[0]
            freq_type = get_frequency_type(text)
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


def get_duration_string(sig):
    words = sig.split()
    for i in range(len(words)):
        if words[i] == 'for':
            return ' '.join(words[i:])
    return None


def convert_fract_to_num(sentence):

    def is_frac(word):
        nums = word.split('/')
        return len(nums) == 2 and '/' in word and nums[0].isdigit() and nums[1].isdigit()

    words = sentence.split()
    output_words = []
    for word in words:
        if is_frac(word):
            num, denom = word.split('/')
            output_words.append(str(int(num)/int(denom)))
        else:
            output_words.append(word)
    return ' '.join(output_words)


def convert_words_to_numbers(sentence):
    words = sentence.split()
    output_words = []
    for word in words:
        if is_number_word(word):
            output_words.append(str(w2n.word_to_num(word)))
        else:
            output_words.append(word)
    return ' '.join(output_words)


def get_single_dose(sig):

    def is_followed_by_number(word):
        dose_istructions = ['take', 'inhale', 'instill', 'apply', 'spray','swallow']
        return word in dose_istructions

    words = sig.split()
    if is_followed_by_number(words[0]) and len(words) > 1 and is_float(words[1]):
        return str(float(words[1]))

    return None

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_frequency_type(frequency):
    if frequency is not None:
        if "day" in frequency or "daily" in frequency:
            return "Day"
        if "week" in frequency:
            return "Week"
        if "month" in frequency:
            return "Month"
        if "night" in frequency:
            return "Day"
        if "morning" in frequency:
            return "Day"
        if "noon" in frequency:
            return "Day"


def get_interval(frequency):
    if frequency is not None:
        for word in frequency.split():
            if word.isdigit():
                return int(word)
        return 1


inp = 'TAKE 1 TABLET TWICE A DAY WITH MEALS for 3 weeks'
# inp = "INHALE 2 PUFFS INTO THE LUNGS EVERY day"
print(parse_sig(inp))