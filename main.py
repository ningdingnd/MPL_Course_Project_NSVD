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
        for dialog in dialogs:
            symblicExecutor.reset(imgIdx)
            # execute the prog. from the caption
            captionFuncLabel = dialog["template"]
          #  print("The caption function is ",captionFuncLabel)
            captionFuncArgs = list(
                map(lambda a: "_".join(a.split(" ")), dialog["args"]))
            
            symblicExecutor.execute(captionFuncLabel, captionFuncArgs)

            # Answer the questions
            for i, d in enumerate(dialog["dialog"]):
               # print("The question is ",i+1,"Question and the content is ",d["question"])
               # print("The type is ",d["template"])
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
         
                   # print("Predict answer",predAnswer)
                   # print("GT answer is ",gtAnswer)
                    numFalse += 1
             
    print("acc = {}".format(1 - numFalse/numAll))

if __name__ == "__main__":
    test()
