# NSVD
This is the original implementation of the neuro-symbolic visual dialog paper, i.e. without the modifications proposed for this project.

## Data
The data (rendered scenes and dialgs) is located in the ```data\``` folder.

## Code
1. Create a conda environment and install dependencies

```shell
   conda create -n nsvd python=3.7
   conda activate nsvd
   conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 cudatoolkit=11.3 -c pytorch
   pip install tqdm h5py tensorboardX
```
2. Preprocess the data
```shell
   cd preprocess_dialogs
   python preprocess # Set the flags as appropriate
   # Note: first create train, val, test folder directly under project, then add three following files ("output_h5.h5", "vocab_input.json", "vocab_output.json") in each of mentioned folders 
   # for gernerating training and validation dataset for stack question program
   python preprocess_dialogs/preprocess.py --input_dialogs_json data/dialogs_train.json --output_vocab_json train/vocab_output.json --output_h5_file train/output_h5.h5 --mode 'stack' --split 'train' --val_size 50 --input_vocab_json train/vocab_input.json 
   python preprocess_dialogs/preprocess.py --input_dialogs_json data/dialogs_train.json --output_vocab_json val/vocab_output.json --output_h5_file val/output_h5.h5 --mode 'stack' --split 'val' --val_size 50 --input_vocab_json val/vocab_input.json 
   # for gernerating test dataset for stack question program
   python preprocess_dialogs/preprocess.py --input_dialogs_json data/dialogs_test.json --output_vocab_json test/vocab_output.json --output_h5_file test/output_h5.h5 --mode 'stack' --split 'test' --val_size 50 --input_vocab_json test/vocab_input.json 

```
3. Adjust the experiments hyperparameters as appropriate in ```prog_generator/options_caption_parser.py``` and ```prog_generator/option_question_parser.py```

4. Train the caption parser

```shell
   cd prog_generator
   python train_caption_parser.py --mode train
```

5. Train the question parser

```shell
   cd prog_generator
   python train_question_parser.py --mode train
```

6. Evaluate

```shell
   cd prog_generator
   python train_question_parser.py --mode test_with_gt
```

## Instructions
1. Read the Neuro-Sybolic Visual Dialog [paper][1]
2. Orient yourself using this codebase and implement the suggested modifications (data preprocessing, dataloaders, model architecture)
3. Train the new seq2seq program generator and evaluate its accuracy, i.e. how accurate the generate programs are
4. Complete the missing modules of the Executor (Re-implementation task)
5. Validate the logic of your exectutor by evaluting it on groud-truth data (scenes and programs) 
6. Test the whole model and compare your results with paper. Here you will use the generated programs and the completed executor

## Important
This README was created to give you an overall picture of how the codease is structured and the main steps you need to follow in order to replicate the results of the paper.
You might need to solve some coding issues on your own if the code does not work out of the bat. This part of the learning process and research in general.

HAPPY CODING!

[1]: https://aclanthology.org/2022.coling-1.17.pdf
