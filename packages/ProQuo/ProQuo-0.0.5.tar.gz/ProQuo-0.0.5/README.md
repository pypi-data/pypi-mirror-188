# Readme
ProQuo is a tool for the detection of short quotations (<= 4 words) between two texts, a source text and a target text.
The target text is the text quoting the source text. Quotations in the target text need to be clearly marked with
quotations marks.

## Overview
The main purpose of this tool is to use the pretrained models for the detection of short quotations.
The library also supports training and testing of custom models for reference classification, relation classification
and linking classification.

## Installation
~~~
pip install ProQuo
~~~

This installs `ProQuo` and all dependencies except `tensorflow` which needs to be installed manually depending on
the individual needs, see [Tensorflow installation](https://www.tensorflow.org/install).

For `RelationModelLstmTrainer`, `tensorflow-text` is needed. `RelationModelLstmTrainer` should normally not be needed as
`RelationModelBertTrainer` performs better and is the default in the pipeline.

## Usage
There are two ways to use the tool: in code and from the command line. Both are described in the following sections.

### Quotation detection
There are two approaches to quotation detection: A specialized pipeline and a general language model based approach.

#### Specialized pipeline
~~~
compare
"path_to_source_text"
"path_to_target_text"
""
""
""
""
--text
--output-type "text"
~~~

#### Language model approach

~~~
proquo compare
""
""
""
""
--text
--output-type "text"
~~~

#### Result
~~~
TBD
~~~


#### Note
There are a number of command line arguments.

~~~
proquo compare -h
~~~

~~~
proquolm compare -h
~~~

~~~
pip install ProQuo
~~~

### Training
 - TBD

### Testing
 - TBD

## Performance
Coming soon!