# Key sentence analytic

This analytic is intended to surface the sentences that are most
relevant within a document. It does this by finding keywords (words
that are often used) within a document and then assigning a sentence
relevance score that is related to the number of key words within a
given sentence. This might be used downstream as a way to filter
sentences by how relevant they are.

This analytic outputs sentence character offsets and a relevance score
from 0 to 1, with 0 being the least relevant and 1 being the
most. This is a normalized score within each document.

[![build and publish](https://github.com/twosixlabs-dart/qntfy-key-sentence/actions/workflows/build-and-publish.yml/badge.svg)](https://github.com/twosixlabs-dart/qntfy-key-sentence/actions/workflows/build-and-publish.yml)

## Delivery information

### Source Code

#### Service or integration code such as REST APIs or web applications

Contained [in this repository](./analytic.py).

#### Source code for model training

Available at the [spacy website][spacy-training].

### Models

#### Inventory of any open source / public models that were used

Available at the [spacy website][spacy-models].

#### Information for how to obtain these models

Consult [this script](./dependencies.sh) or above site.

### Documentation

#### Reference information on the model or algorithm that is used for each analytic

Available at the [spacy website][spacy-models].

#### Documentation on how to train and deploy new models

Available at the [spacy website][spacy-training].

#### Information on data cleaning, preparation, or formatting that is required for each model

Available at the [spacy website][spacy-models].

### Data

No models were trained with provided data.

[spacy-training]: https://spacy.io/usage/training
[spacy-models]: https://spacy.io/models/en
