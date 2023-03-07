import pathlib

from spacy.tokens import DocBin
import spacy

# globally picking a subset of labels
INCL_LABELS = ['Dosage', 'Drug', 'Form', 'Frequency']

def main():

    input_path = pathlib.Path("/Users/royashcenazi/downloads/training_20180910")
    output_path = pathlib.Path("/Users/royashcenazi/downloads/first_trial.spacy")
    nlp = spacy.blank("en")
    doc_bin = DocBin(attrs=["ENT_IOB", "ENT_TYPE"])
    # get all ann
    # match ann and txt
    ann_txt = {}
    for a in input_path.glob('*.ann'):
        match = list(input_path.glob(f'{a.stem}.txt'))
        if len(match) > 1:
            raise ValueError(f'Multiple matches for ann file {a}')
        elif len(match) == 0:
            raise ValueError(f'No match for ann file {a}')
        ann_txt[a] = match[0]
    for a in ann_txt:
        txt = ann_txt[a].read_text()
        doc = nlp(txt)
        ents = []
        for l in a.read_text().split('\n'):
            ann = l.split('\t')
            if len(ann) != 3:
                continue
            ann_type, label_idx, text = ann
            # just want text annotations, not relations
            if ann_type[0] != 'T':
                continue
            # cases of line splits indicated by semicolons - just take whole span
            elif ';' in label_idx:
                label_idx_filtered = []
                for el in label_idx.split():
                    if ';' in el:
                        continue
                    label_idx_filtered.append(el)
                label, st, end = label_idx_filtered
            else:
                label, st, end = label_idx.split()
            if label in INCL_LABELS:
                ents.append([st, end, label])
        # some spans are invalid - don't match spacy's tokenization, for now, drop those entities
        ents_filtered = []
        for e in ents:
            span = doc.char_span(int(e[0]), int(e[1]), label=e[2])
            if span:
                ents_filtered.append(span)
        # additionally some overlap, prefers longer spans
        ents_filtered = spacy.util.filter_spans(ents_filtered)
        doc.ents = ents_filtered
        doc_bin.add(doc)
    doc_bin.to_disk(output_path)
    print(f"Processed {len(doc_bin)} documents: {output_path.name}")


if __name__ == "__main__":
    main()