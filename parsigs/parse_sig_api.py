import sys

import spacy
from word2number import w2n
from dataclasses import dataclass
import re
import logging
from spacy import Language


# TODO handle multiple instructions in one sentence
# TODO convert form to singular if plural using Spacy
# TODO github workflow to run unit tests
# TODO Create Pypi distribution
# TODO add as_needed flag

"""
Represents a structured medication dosage instructions.
Attributes:
-----------
drug : str
    The name of the medication drug.
form : str
     The form of the medication (e.g. tablet, capsule, injection).
strength : str
    The strength of the medication (e.g. 10mg, 20mg).
frequencyType : str
    The type of frequency for the dosage (e.g. Hour, Day, Week, Month).
interval : int
     The interval between dosages (e.g. every 4 hours, every 12 hours, etc.).
singleDosageAmount : int
    The amount of the medication in a single dosage (e.g. 1 tablet, 2 capsules, etc.).
periodType : str
    The type of period for the dosage (e.g. Hour, Day, Week, Month).
periodAmount : int
    The duration of the period for the dosage (e.g. 7 days, 2 months, etc.).
"""


@dataclass
class StructuredSig:
    drug: str
    form: str
    strength: str
    frequencyType: str
    interval: int
    singleDosageAmount: float
    periodType: str
    periodAmount: int


dose_instructions = ['take', 'inhale', 'instill', 'apply', 'spray', 'swallow']
number_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

default_model_path = "{}/research/sig_ner_model/model-best".format(sys.path[0])

"""
Converts a medication dosage instructions string to a StructuredSig object.
The input string is pre processed, and than combining static rules and NER model outputs, a StructuredSig object is created.
"""


def parse_sig(sig: str, model_path=default_model_path):
    model = spacy.load(model_path)
    return _parse_sig(sig, model)


def parse_sigs(sig_lst: list[str], model_path=default_model_path):
    model = spacy.load(model_path)
    return list(map(lambda sig: _parse_sig(sig, model), sig_lst))


def _parse_sig(sig: str, model: Language):
    sig_preprocessed = _pre_process(sig)
    model_output = model(sig_preprocessed)

    logging.debug("model output: ", [(e, e.label_) for e in model_output.ents])

    return _create_structured_sig(model_output, sig_preprocessed)


def _pre_process(sig):
    sig = sig.lower().replace('twice', '2 times').replace("once", '1 time')

    sig = _add_space_around_parentheses(sig)

    # remove extra spaces between words
    sig = re.sub(r'\s+', ' ', sig)

    output_words = []
    words = sig.split()
    for word in words:
        if word == 'tab':
            word = word.replace('tab', 'tablet')
        else:
            output_words.append(word)
    sig = ' '.join(output_words)

    sig = _convert_words_to_numbers(sig)
    return _convert_fract_to_num(sig)


def _add_space_around_parentheses(s):
    s = re.sub(r'(?<!\s)\(', r' (', s)
    s = re.sub(r'\)(?!\s)', r') ', s)
    return s


"""
Converts the preprocessed sig using static rules and the model outputs
"""


def _create_structured_sig(model_output, sig_preprocessed):
    duration_string = _get_duration_string(sig_preprocessed)
    # The initial values using helper methods are only when them model does not detect the entity (otherwise the detected entity is used)
    dosage, drug, form, freq_type, interval, period_type, period_amount, strength = \
        _get_single_dose(sig_preprocessed), None, None, None, None, _get_frequency_type(duration_string), \
        _get_interval(duration_string), None

    entities = _get_model_entities(model_output)

    for entity in entities:
        text = entity.text
        label = entity.label_
        if label == 'Dosage' and text.split()[0].isnumeric():
            dosage = float(text.split()[0])
            freq_type = _get_frequency_type(text)
        if label == 'Drug':
            drug = text
        if label == 'Form':
            form = text
        if label == 'Frequency':
            freq_type = _get_frequency_type(text)
            interval = _get_interval(text)
        if label == 'Duration':
            period_type = _get_frequency_type(text)
            period_amount = _get_interval(text)
        if label == 'Strength':
            strength = text
    return StructuredSig(drug, form, strength, freq_type, interval, dosage, period_type, period_amount)


"""
There is a known issue where the model wrongly tag sometimes frequency as dosage signatures, this is a current fix
as the last tag should not be dosage instruction, remove this once training data is fixed to handle such issue
"""


def _get_model_entities(model_output):
    entities = model_output.ents
    if entities[-1].label_ == "Dosage":
        entities[-1].label_ = "Frequency"
    return entities
def _is_number_word(word):
    return word in number_words


def _get_duration_string(sig):
    words = sig.split()
    for i in range(len(words)):
        if words[i] == 'for':
            return ' '.join(words[i:])
    return None


def _convert_fract_to_num(sentence):

    def is_frac(_word):
        nums = _word.split('/')
        return len(nums) == 2 and '/' in _word and nums[0].isdigit() and nums[1].isdigit()

    words = sentence.split()
    output_words = []
    for word in words:
        if is_frac(word):
            num, denom = word.split('/')
            output_words.append(str(int(num)/int(denom)))
        else:
            output_words.append(word)
    return ' '.join(output_words)


def _convert_words_to_numbers(sentence):
    words = sentence.split()
    output_words = []
    for word in words:
        if _is_number_word(word):
            output_words.append(str(w2n.word_to_num(word)))
        else:
            output_words.append(word)
    return ' '.join(output_words)


def _get_single_dose(sig):

    def is_followed_by_number(word):
        return word in dose_instructions

    words = sig.split()
    if is_followed_by_number(words[0]) and len(words) > 1 and _is_str_float(words[1]):
        return float(words[1])

    return None


def _is_str_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def _get_frequency_type(frequency):
    if frequency is not None:
        if "hour" in frequency:
            return "Hour"
        if "week" in frequency:
            return "Week"
        if "month" in frequency:
            return "Month"
        if any(daily_instruction in frequency for daily_instruction in ("day", "daily", "night", "morning", "noon", "bedtime")):
            return "Day"


def _get_interval(frequency):
    if frequency is not None:
        for word in frequency.split():
            if word.isdigit():
                return int(word)
        return 1


