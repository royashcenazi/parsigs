# Parsigs - Private, Smart, and Easy Sig (Dosage Instructions) Text Parser

[![GitHub stars](https://img.shields.io/github/stars/royashcenazi/parsigs)](https://github.com/royashcenazi/parsigs/stargazers)
[![GitHub license](https://img.shields.io/github/license/royashcenazi/parsigs)](https://github.com/royashcenazi/parsigs/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/royashcenazi/parsigs)](https://github.com/royashcenazi/parsigs/issues)
[![GitHub last commit](https://img.shields.io/github/last-commit/royashcenazi/parsigs)](https://github.com/royashcenazi/parsigs/commits/main)

Parsigs is an open-source project that aims to extract relevant information from doctors' signature text without compromising privacy and PHI (Protected Health Information) using Natural Language Processing.

## Table of Contents
- [Introduction](#introduction)
- [Call for Contributors](#call-for-contributors)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Known Issues](#known-issues)
- [Contributing](#contributing)
- [Credits](#credits)

## Introduction
Parsigs is a powerful and privacy-conscious text-parser designed to extract essential information such as dosage, frequency, and drug names from doctors' prescription-sig text. The primary objective of Parsigs is to facilitate the extraction of structured dosage instructions while ensuring patient privacy by not extracting any patient-related information or using external APIs. By utilizing advanced Natural Language Processing techniques, Parsigs accurately extracts vital details from unstructured text, enabling healthcare professionals to interpret prescription information more efficiently.

## Call for Contributors
We welcome contributions from developers and researchers interested in enhancing Parsigs. Whether it's fixing bugs, adding new features, or improving documentation, your input is valuable to us. If you'd like to participate in the development and maintenance of this project, please feel free to open a pull request or an issue. Thank you to all the contributors who have already contributed to the project!

## Features
- Extracts relevant structured information such as dosage, frequency, and drug names from doctors' prescription-sig text.
- Protects patient privacy by not extracting any patient-related information or utilizing any external APIs.
- Utilizes NLP techniques to accurately extract information from unstructured text.

## Installation
For optimal usage, you will need to install the `parsigs` package and the underlying model. We recommend using the pre-trained model for parsing dosage instructions from Sigs.

```bash
pip install parsigs
pip install https://huggingface.co/royashcenazi/en_parsigs/resolve/main/en_parsigs-any-py3-none-any.whl
```

## Usage
Using Parsigs is straightforward. Here are some examples of how to use the `parse_sig` method:

```python
from parsigs.parse_sig_api import StructuredSig, SigParser

sig_parser = SigParser()

sig = "Take 1 tablet of ibuprofen 200mg 3 times every day for 3 weeks"
parsed_sig = sig_parser.parse(sig)

expected = StructuredSig(drug="ibuprofen", form="tablet", strength="200mg", frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType='Week', periodAmount=3, takeAsNeeded=False)

sig2 = "Take 2 tablets 3 times every month"
parsed_sig = sig_parser.parse(sig2)

expected = StructuredSig(drug=None, form='tablets', strength=None, frequencyType='Month', interval=3, singleDosageAmount=2.0, periodType=None, periodAmount=None, takeAsNeeded=False)
```

The `StructuredSig` object has the following attributes:
- `drug`: the name of the drug
- `form`: the form of the medication (e.g. tablet, solution, pill)
- `strength`: the strength of the medication (e.g. 200mg, 500mg)
- `frequencyType`: the time-unit of the frequency (e.g. Day, Week, Month)
- `interval`: the number of times per frequency time-unit
- `singleDosageAmount`: the amount of the medication to take at each interval
- `periodType`: the unit-type of the period which indicates for how long medication should be taken (e.g. Day, Week, Month)
- `periodAmount`: the number of units per `periodType`
- `takeAsNeeded`: a flag indicating if the instructed dosage should be taken only when the patient needs it

## Known Issues
The parse-sig project is developed using the Named Entity Recognition (NER) model for tagging different parts in a dosage instruction (Sig) sentence, including Duration, Frequency, Dosage, Drug, Form, and Strength. These tags are then processed using static rules. Due to the limited availability of private dosage data, some errors may be expected in the extracted information. The project is constantly evolving, and the developer plans to add a Dev set in the future along with more examples to improve accuracy.

While Parsigs aims to identify and structure dosage instructions effectively, it's worth noting that the identification of brand names as part of the definition may not be as complete as the extraction of frequency, dosage, and period information (as this data is often not explicitly provided in the Sig, e.g., "Take 1 tablet every day").

## Contributing
We encourage contributions to improve Parsigs. If you encounter any issues or have any questions, please don't hesitate to reach out to us by email or file an issue on our GitHub repository.

## Credits
This project builds upon the work of several resources, including:
- [Training a Medication Named Entity Recognition Model from Scratch with SpaCy](https://odsc.medium.com/training-a-medication-named-entity-recognition-model-from-scratch-with-spacy-e94fdff56022)
- [GitHub - bpben/spacy_ner_tutorial](https://github.com/bpben/spacy_ner_tutorial)
