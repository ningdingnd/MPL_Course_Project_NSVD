import os
import json
from utils import load_clevr_scenes
from executor.symbolic_executor import SymbolicExecutorClevr

from tqdm import tqdm

path_scenes_raw = os.path.join(os.getcwd(), "data/CLEVR_scenes.json")
path_dataset = os.path.join(os.getcwd(),"data/dialogs.json")
with open(path_dataset, "r") as file:
    dataset = json.load(file)

symblicExecutor = SymbolicExecutorClevr(path_scenes_raw)
scenes = load_clevr_scenes(path_scenes_raw)

def test():
    numFalse = 0
    numAll = 0
    pbar = tqdm(dataset)
    pbar.set_description("[Evaluation in Progress]")
    for img in pbar:
        imgIdx = img["image_index"]
        dialogs = img["dialogs"]
        dIdx = 0
        # print("img index:", imgIdx)
        for dialog in dialogs:
            symblicExecutor.reset(imgIdx)
            # execute the prog. from the caption
            captionFuncLabel = dialog["template"]
            captionFuncArgs = list(
                map(lambda a: "_".join(a.split(" ")), dialog["args"]))
            
            symblicExecutor.execute(captionFuncLabel, captionFuncArgs)
            # print('CAP', dialog['caption'], dialog['template'], captionFuncArgs)         
            # Answer the questions
            for i, d in enumerate(dialog["dialog"]):
                gtAnswer = "_".join(str(d["answer"]).split(" "))
                # print("QUES",i,d["question"],d["template"], d['args'], gtAnswer)
                
                # if i+1 == 10:
                #     print("bla")
                numAll += 1
                questionFuncLabel = d["template"]
                questionFuncArgs = list(
                    map(lambda a: "_".join(a.split(" ")), d["args"]))
                gtAnswer = "_".join(str(d["answer"]).split(" "))
                predAnswer = symblicExecutor.execute(
                    questionFuncLabel, questionFuncArgs)
                predAnswer = str(predAnswer)
                if predAnswer != gtAnswer:
         
                   # print("PRED answer",predAnswer)
                    numFalse += 1
             
    print("acc = {}".format(1 - numFalse/numAll))

if __name__ == "__main__":
    test()
