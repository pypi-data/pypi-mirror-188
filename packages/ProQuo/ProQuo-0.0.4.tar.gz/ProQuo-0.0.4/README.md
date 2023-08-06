# Readme

ProQuo is a tool for the detection of short quotations (<= 4 words) between two texts, a source text and a target text.
The target text is the text quoting the source text. Quotations in the target text need to be clearly marked with
quotations marks.

## Overview
TBD

## Installation
~~~
pip install ProQuo
~~~

This installs `ProQuo` and all dependencies except `tensorflow` which needs to be installed manually depending on
the individual needs, see [Tensorflow Install](https://www.tensorflow.org/install).

For `RelationModelLstmTrainer`, `tensorflow-text` is needed. `RelationModelLstmTrainer` should normally not be needed as
`RelationModelBertTrainer` performs better and is the default in the pipeline.

## Usage
There are two ways to use the tool. The following two sections describe the use of the algorithm in code and from the command line.

### Quotation detection

### Training
 - TBD

### Testing
 - TBD

## Performance