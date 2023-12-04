# Instructions

## Data
1. The data needed for this re-implementation task is located in the ```data/``` folder.
2. There you can find the raw dialogs with the ground truth caption and question programs (```data/dialogs.json```) and the derendered scenes on top of which the programs will be executed (```data/CLEVR_scenes.json```).

## Code
............

## Task
Some functions of the executor are missing. The main goal of this task is to re-implement these based on the NSVD [paper][1] and the remaining methods of the executor. Please take a look at ```executor/symbolic_executor.py``` and complete the missing modules. These are marked with "TODO".

## Goal
Once you are happy with the code, run the evaluation script, i.e. ```main.py```, to test you implemented logic. You should get an accuracy close to that in Table 6 of the [paper][1], i.e. 99.99%

HAPPY CODING!

[1]: https://perceptualui.org/publications/abdessaied22_coling.pdf
