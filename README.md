# NLP robustness test

## Table of Content
1. [Overview](#overview)

## Overview
This package evaluates the robustness of NLP (classification) models from the perspective of behavioral tests and adversarial examples, utilizing [CheckList](https://github.com/marcotcr/checklist) and [TextAttack](https://github.com/QData/TextAttack)

1. git clone
2. cd into nlp_test
3. 
```
docker build -f ./docker/Dockerfile --tag nlp_test:0.0.1 --network=host .
```
