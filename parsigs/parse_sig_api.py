import sys

import spacy
from word2number import w2n
from dataclasses import dataclass
import re
import logging
from spacy import Language

# TODO handle multiple instructions in one sentence
# TODO convert form to singular if plural using Spacy
# TODO Create Pypi distribution

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
takeAsNeeded : bool
    Some instructions contains a statement that the medication should be taken as needed by patient
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
    takeAsNeeded: bool


dose_instructions = ['take', 'inhale', 'instill', 'apply', 'spray', 'swallow']
number_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

default_model_name = "en_parsigs"

@dataclass(frozen=True, eq=True)
class _Frequency:
    frequencyType: str
    interval: int


# TODO add qXd support
latin_frequency_types = {"qd": _Frequency("Day", 1), "bid": _Frequency("Day", 2), "tid": _Frequency("Day", 3),
                         "qid": _Frequency("Day", 4)}

"""
Converts a medication dosage instructions string to a StructuredSig object.
The input string is pre processed, and than combining static rules and NER model outputs, a StructuredSig object is created.
"""


def _parse_sigs(sig_lst, model: Language):
    return list(map(lambda sig: _parse_sig(sig, model), sig_lst))


def _parse_sig(sig: str, model: Language):
    sig_preprocessed = _pre_process(sig)
    model_output = model(sig_preprocessed)

    logging.debug("model output: ", [(e, e.label_) for e in model_output.ents])

    return _create_structured_sig(model_output, sig_preprocessed)


def _pre_process(sig):
    sig = sig.lower().replace('twice', '2 times').replace("once", '1 time').replace("nightly", "every night")

    sig = _add_space_around_parentheses(sig)

    # remove extra spaces between words
    sig = re.sub(r'\s+', ' ', sig)

    output_words = []
    words = sig.split()
    for word in words:
        if word == 'tab':
            word = word.replace('tab', 'tablet')
            output_words.append(word)
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
    dosage, drug, form, freq_type, interval, period_type, period_amount, strength, take_as_needed = \
        _get_single_dose(sig_preprocessed), None, None, None, None, _get_frequency_type(duration_string), \
        _get_interval(duration_string), None, False

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
            # Default added only if there is a frequency tag in the sig, handles cases such as "Every TIME_UNIT"
            if interval is None:
                interval = 1
            take_as_needed = _should_take_as_needed(text)
        if label == 'Duration':
            period_type = _get_frequency_type(text)
            period_amount = _get_interval(text)
        if label == 'Strength':
            strength = text
    return StructuredSig(drug, form, strength, freq_type, interval, dosage, period_type, period_amount, take_as_needed)


def _get_model_entities(model_output):
    entities = model_output.ents
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
            output_words.append(str(int(num) / int(denom)))
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
        if any(daily_instruction in frequency for daily_instruction in
               ("day", "daily", "night", "morning", "evening", "noon", "bedtime")):
            return "Day"
        latin_freq = _get_latin_frequency(frequency)
        if latin_freq:
            return latin_freq.frequencyType


def _get_interval(frequency):
    if frequency is not None:
        for word in frequency.split():
            if word.isdigit():
                return int(word)
        # every other TIME_UNIT means every 2 days,weeks etc
        if "other" in frequency:
            return 2
        latin_freq = _get_latin_frequency(frequency)
        if latin_freq:
            return latin_freq.interval


def _get_latin_frequency(frequency):
    for latin_freq in latin_frequency_types.keys():
        if latin_freq in frequency:
            return latin_frequency_types[latin_freq]


def _should_take_as_needed(frequency):
    return "as needed" in frequency


class SigParser:
    def __init__(self, model_name="en_parsigs"):
        self.__language = spacy.load(model_name)

    def parse(self, sig: str):
        return _parse_sig(sig, self.__language)

    def parse_many(self, sigs: list):
        return _parse_sigs(sigs, self.__language)

