import sys
from pathlib import Path

import spacy
from word2number import w2n
import re
from spacy import Language
from itertools import chain
from dataclasses import dataclass, replace
import copy
import os
from spellchecker import SpellChecker
import json
import inflect

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
    singleDosageAmount: float
    periodType: str
    periodAmount: int
    times: int
    interval: int = 1
    takeAsNeeded: bool = False


dose_instructions = ['take', 'inhale', 'instill', 'apply', 'spray', 'swallow']
number_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]

default_model_name = "en_parsigs"

inflect_engine = inflect.engine()


def _open_latin_type_dict():  # add parameters path, name
    latin_frequency_file_path = Path(__file__).parent / 'resources/latin_frequency.json'
    with open(latin_frequency_file_path, 'r') as latin_file:
        return json.load(latin_file)


latin_type_dict = _open_latin_type_dict()


def _create_spell_checker():
    sc = SpellChecker()
    drug_words_frequency = Path(__file__).parent / 'resources/drug_names.txt'
    sc.word_frequency.load_text_file(drug_words_frequency)
    sc.word_frequency.remove_words(["talbot"])
    return sc


spell_checker = _create_spell_checker()


def _flatmap(func, iterable):
    return list(chain.from_iterable(map(func, iterable)))


"""
Converts a medication dosage instructions string to a StructuredSig object.
The input string is pre processed, and than combining static rules and NER model outputs, a StructuredSig object is created.
"""


def _parse_sigs(sig_lst, model: Language):
    return _flatmap(lambda sig: _parse_sig(sig, model), sig_lst)


def _parse_sig(sig: str, model: Language):
    sig_preprocessed = _pre_process(sig)
    model_output = model(sig_preprocessed)

    return _create_structured_sigs(model_output)


def _autocorrect(sig):
    sig = sig.lower().strip()
    corrected_words = []
    for word in sig.split():
        # checking if the word is only letters
        if not re.match(r"^[a-zA-Z]+$", word) or spell_checker.known([word]):
            corrected_words.append(word)
        else:
            corrected_word = spell_checker.correction(word)
            corrected_words.append(corrected_word)
    sig = ' '.join(corrected_words)
    return sig


def _pre_process(sig):
    sig = _autocorrect(sig)
    sig = sig.replace('twice', '2 times').replace("once", '1 time').replace("nightly", "every night")
    sig = _add_space_around_parentheses(sig)
    # remove extra spaces between words
    sig = re.sub(r'\s+', ' ', sig)
    output_words = []
    words = sig.split()
    for word in words:
        if word == 'tab':
            word = word.replace('tab', 'tablet')
        elif word == 'tabs':
            word = word.replace('tabs', 'tablet')
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


def _split_entities_for_multiple_instructions(model_entities):
    result = []

    seen_labels = set()
    current_sublist = []
    for entity in model_entities:
        if entity.label_ in seen_labels:
            result.append(current_sublist)
            current_sublist = []
            seen_labels.clear()

        current_sublist.append(entity)
        seen_labels.add(entity.label_)

    result.append(current_sublist)
    return result


def _create_structured_sigs(model_output):
    entities = _get_model_entities(model_output)

    multiple_instructions = _split_entities_for_multiple_instructions(entities)

    first_sig = _create_structured_sig(multiple_instructions[0])

    # incase multiple instructions exist, they apply to the same drug and form
    other_sigs = [_create_structured_sig(instruction_entities, first_sig.drug, first_sig.form)
                  for instruction_entities in multiple_instructions[1:]]
    return [first_sig] + other_sigs


def _get_form_from_dosage_tag(text):
    splitted = text.split(' ')
    if len(splitted) == 2:
        return splitted[1]


def _to_singular(text):
    # turn to singular if plural else keep as is
    singular = inflect_engine.singular_noun(text)
    return singular if singular else text


def _create_structured_sig(model_entities, drug=None, form=None):
    structured_sig = StructuredSig(drug, form, None, None, None, None, None, None)

    for entity in model_entities:
        text = entity.text
        label = entity.label_
        if label == 'Dosage' and text.split()[0].isnumeric():
            structured_sig.singleDosageAmount = float(text.split()[0])
            structured_sig.frequencyType = _get_frequency_type(text)
            form_from_dosage = _get_form_from_dosage_tag(text)
            if form_from_dosage is not None:
                structured_sig.form = _to_singular(form_from_dosage)
        elif label == 'Drug':
            structured_sig.drug = text
        elif label == 'Form':
            structured_sig.form = _to_singular(text)
        elif label == 'Frequency':
            structured_sig.frequencyType = _get_frequency_type(text)
            interval_text = _get_string_after_keyword(text, "every")
            if len(interval_text) > 0:
                structured_sig.interval = _get_amount_from_frequency_tags(interval_text)
            latin_frequency_dict = _get_latin_frequency(text)
            if latin_frequency_dict:
                # we assume that the latin_frequency_dict values are a dict of frequencyType, interval and times
                structured_sig = replace(structured_sig, **latin_frequency_dict)
            else:
                times_text = _get_string_until_keyword(text, "times")
                structured_sig.times = _get_amount_from_frequency_tags(times_text)
            # Default added only if there is a frequency tag in the sig, handles cases such as "Every TIME_UNIT"
            if structured_sig.interval is None:
                structured_sig.interval = 1
            structured_sig.takeAsNeeded = _should_take_as_needed(text)
        elif label == 'Duration':
            structured_sig.periodType = _get_frequency_type(text)
            structured_sig.periodAmount = _get_amount_from_frequency_tags(text)
        elif label == 'Strength':
            structured_sig.strength = text
    return structured_sig


def _get_string_after_keyword(input_string: str, keyword: str):
    keyword_index = input_string.find(keyword)
    if keyword_index != -1:
        return input_string[keyword_index + len(keyword):].strip()
    return ""


def _get_string_until_keyword(input_string: str, keyword: str):
    keyword_index = input_string.find(keyword)
    if keyword_index != -1:
        return input_string[:keyword_index].strip()
    return ""


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
        if "year" in frequency:
            return "Year"
        if any(daily_instruction in frequency for daily_instruction in
               ("day", "daily", "night", "morning", "evening", "noon", "bedtime")):
            return "Day"


def _get_amount_from_frequency_tags(frequency):
    if frequency is not None:
        for word in frequency.split():
            if word.isdigit():
                return int(word)
        # every other TIME_UNIT means every 2 days,weeks etc
        if "other" in frequency:
            return 2


def _get_latin_frequency(frequency: str):
    stripped_freq = frequency.split()[0].replace('.', '')
    return latin_type_dict.get(stripped_freq) if latin_type_dict.get(stripped_freq) else None


def _should_take_as_needed(frequency):
    return "as needed" in frequency


class SigParser:
    def __init__(self, model_name="en_parsigs"):
        self.__language = spacy.load(model_name)

    def parse(self, sig: str):
        return _parse_sig(sig, self.__language)

    def parse_many(self, sigs: list):
        return _parse_sigs(sigs, self.__language)
