#!/usr/bin/env python3

import sys
import os
import logging
import json

import falcon
import spacy

from ceeder import TagAnnotator

import re
from typing import List, Dict
from string import punctuation
from collections import Counter


LABEL="Qntfy Key Sentences"


@spacy.Language.component("custom_splitters")
def custom_splitters(doc):
    """ Define additional (missing in defaults) sentence splitters:
    - Bullet character
    - Footnotes (formatted as string, e.g., 'end of sentence.1 Beginning of sentence...')
    - Newline
    """

    for token in doc[:-1]:
        if token.text in (u"\u2022"):
            doc[token.i].is_sent_start = True
            continue

        if re.search("\\.[0-9]", str(token.text)):
            doc[token.i+1].is_sent_start = True
            continue

        if "\n" in token.text:
            doc[token.i+1].is_sent_start = True
            continue

    return doc

nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("custom_splitters", before="parser")

max_length = os.getenv("MAX_DOCUMENT_LENGTH")
if max_length:
    nlp.max_length = int(max_length)

MIN_SENTENCE_LENGTH = 80 # Minimum length (in characters) to receive a score


def txt_to_cdr_tags(txt: str):
    keyword = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
    doc = nlp(txt)
    for token in doc:
        if(token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            keyword.append(token.text)

    freq_word = Counter(keyword)
    max_freq = Counter(keyword).most_common(1)[0][1]
    for w in freq_word:
        freq_word[w] = (freq_word[w]/max_freq)

    sent_strength={}
    sentences = []
    for sent in doc.sents:
        sent_dict = {}
        sent_dict['offset_start'] = sent.start_char
        sent_dict['offset_end'] = sent.end_char
        sent_dict["tag"] = "KEY_SENTENCE"

        if len(str(sent)) < MIN_SENTENCE_LENGTH:
            sent_dict['score'] = 0
            sentences.append(sent_dict)

        else:
            for word in sent:
                if word.text in freq_word.keys():
                    if sent in sent_strength.keys():
                        sent_strength[sent]+=freq_word[word.text]
                    else:
                        sent_strength[sent]=freq_word[word.text]

                    sent_dict['score'] = sent_strength[sent]

            sentences.append(sent_dict)

    values = [d['score'] for d in sentences if 'score' in d]

    maximum = max(values)
    minimum = min(values)

    # guard against divide by zero
    difference = float(maximum-minimum)
    if difference == 0:
        difference = 1

    sentences_new = [{a:b if a != "score" else (b-minimum)/difference for a, b in i.items()} for i in sentences]
    with_label = filter((lambda x: 'score' in x), sentences_new)

    return list(with_label), falcon.HTTP_200


def create():
    tag_anno = TagAnnotator(
        txt_to_cdr_tags,
        label=LABEL,
    )

    return tag_anno.create()
