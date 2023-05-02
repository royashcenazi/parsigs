import pathlib

from spacy.tokens import DocBin
import spacy

# globally picking a subset of labels
INCL_LABELS = ['Dosage', 'Drug', 'Form', 'Frequency', 'Strength', 'Duration']

def main():

    input_path = pathlib.Path("training_20180910")
    output_path_train = pathlib.Path("train_docs.spacy")
    output_path_test = pathlib.Path("test_docs.spacy")
    nlp = spacy.blank("en")
    doc_bin_train = DocBin(attrs=["ENT_IOB", "ENT_TYPE"])
    doc_bin_test = DocBin(attrs=["ENT_IOB", "ENT_TYPE"])
    doc_list = []
    # get all ann
    # match ann and txt
    ann_txt = {}
    for annotation_file in input_path.glob('*.ann'):
        matched_text = list(input_path.glob(f'{annotation_file.stem}.txt'))
        if len(matched_text) > 1:
            raise ValueError(f'Multiple matches for ann file {annotation_file}')
        elif len(matched_text) == 0:
            raise ValueError(f'No match for ann file {annotation_file}')
        ann_txt[annotation_file] = matched_text[0]
    for text_file in ann_txt:
        txt = ann_txt[text_file].read_text()
        doc = nlp(txt)
        ents = []
        for l in text_file.read_text().split('\n'):
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
        doc_list.append(doc)
    
    # split into train and tests
    train_docs = doc_list[:int(len(doc_list)*0.9)]
    test_docs = doc_list[int(len(doc_list)*0.9):]

    # add to doc_bin
    for doc in train_docs:
        doc_bin_train.add(doc)
    for doc in test_docs:
        doc_bin_test.add(doc)

    doc_bin_test.to_disk(output_path_test)
    doc_bin_train.to_disk(output_path_train)
    print(f"Processed {len(doc_list)} documents")


if __name__ == "__main__":
    main()
