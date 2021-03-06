# NLP robustness test

## Table of Content
1. [Overview](#overview)
2. [Dependencies](#dependencies)
3. [Usage](#usage)
4. [Docker Image](#docker-image)

## Overview
This package evaluates the robustness of NLP (classification) models from the perspective of behavioral tests and adversarial examples, utilizing [CheckList](https://github.com/marcotcr/checklist) and [TextAttack](https://github.com/QData/TextAttack)

## Dependencies
Most dependencies are listed in the requirement file.
1. language-tool-python requires Java 8

## Usage

### Inputs

1. tokenizer: a tokenizer that tokenizes the sentences and turns tokens into word indices
2. model: a model that takes tokenized sentences and produces class probabilities
3. data: an iterable of sentence label pairs
4. config file (YAML) : a config file in YAML format that describes the tests to run the attack method to use

### Output
A report summarizing test results and adversarial examples.

### Example
Refer to the test case `test_report` in tests/test_report.py for an example of how to use this package.

To start, define a NLPReport by 
```
from nlptest.nlptest.nlp_report import NLPReport
```
and provide inputs as arguments
```
report = NLPReport(dataset=dataset, model=model, tokenizer=tokenizer,
                   config_file=current_path / "config_test.yaml")
```
Results can be inspected in the `test_result` attribute
```
report.test_result
```
Currently implemented output formats include:
* HTML: `report.html`
* JSON: `report.json`
* dictionary: `report.dict`

Refer to `tests/config_test.yaml` and `nlpteste/nlptest/` for examples of test configuration.

## Docker Image
1. git clone
2. cd into nlp_test
3. 
```
docker build -f ./docker/Dockerfile --tag nlp_test:0.0.1 --network=host .
```
