# Parsigs - the private, smart and easy Sig (Dosage Instructions) text-parser 

Parsigs is an open-source project that aims to extract relevant information from doctors' signature text without compromising privacy and PHI (Protected Health Information) using Natural Language Processing.

## Features

- Extracts relevant structured information such as dosage, frequency, drug name from doctors' prescription-sig text.
- Protects patient privacy by not extracting any patient-related information or using any external API.
- Uses NLP techniques to accurately extract information from unstructured text.


## Usage
Here are some examples of how to use the parse_sig method:


```
from parsigs.parse_sig_api import StructuredSig, parse_sig

sig = "Take 1 tablet of ibuprofen 200mg 3 times every day for 3 weeks"
parsed_sig = parse_sig(sig)

expected = StructuredSig(drug="ibuprofen", form="tablet", strength="200mg", frequencyType="Day", interval=3, singleDosageAmount=1.0, periodType='Week', periodAmount=3)

sig2 = "Take 2 tablets 3 times every month"
parsed_sig = parse_sig(sig)

expected = StructuredSig(drug=None, form='tablets', strength=None, frequencyType='Month', interval=3, singleDosageAmount=2.0, periodType=None, periodAmount=None)

```

The `StructuredSig` object has the following attributes:

* `drug`: the name of the drug
* `form`: the form of the medication (e.g. tablet, solution, pill)
* `strength`: the strength of the medication (e.g. 200mg, 500mg)
* `frequencyType`: the time-unit of the frequency (e.g. Day, Week, Month)
* `interval`: the number of times per frequency time-unit
* `singleDosageAmount`: the amount of the medication to take at each interval
* `periodType`: the unit-type of the period which indicates for how long medication should be taken (e.g. Day, Week, Month)
* `periodAmount`: the number of units per `periodType` 

If you encounter any issues or have any questions, please don't hesitate to send me an email or file an issue.


## Credits
This repository is based on the following resources - 

https://odsc.medium.com/training-a-medication-named-entity-recognition-model-from-scratch-with-spacy-e94fdff56022

https://github.com/bpben/spacy_ner_tutorial