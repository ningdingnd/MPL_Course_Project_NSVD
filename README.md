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

## Problem 
In seekAttributeRelEarly() ```earlyObj = deepcopy(filtered_earlyObjs[-2]) ``` if there are more than one obj in the earlyObj and also fulfill the attribute filter and the curren obj = early obj we dont know which one should choose it to be the early Obj is the last one or the last two. We set it to ``` [-2]``` since it has higher accuracy. 


## 3-6 should be -2 
dialog 3
caption: 'There are 2 cylinders in the image.' 'count-att'
0. 'Any green objects in the group?''yes''exist-attribute-group'['green']
1.'What is the count of other objects in the image?'3'count-other'
2.'If there is an object to the left of the earlier green object, what is its material?''rubber''seek-attr-rel-early'
3.'What is the size of this object?''large''seek-attr-imm'['size']
4.'And color?''brown''seek-attr-imm2'['color']
5.'If there is an object right of the above green object, what material is it?''rubber''seek-attr-rel-early'['material', 'right', 'green']
6.'What is the count of objects the earlier large object has to its front?'2 count-obj-rel-early'['front', 'large']

## 2-8 should be -1
QUES 0 If there is an object left of it, what is its shape? seek-attr-rel-imm ['shape', 'left'] none
QUES 1 How many other objects share similar color with that brown object? count-obj-exclude-early ['color', 'brown'] 0
QUES 2 If there is an object behind the earlier brown object, what is its material? seek-attr-rel-early ['material', 'behind', 'brown'] rubber
QUES 3 If there is an object in front of that brown object, what is its size? seek-attr-rel-early ['size', 'front', 'brown'] small
QUES 4 If there is an object to the right of the previous matte object, what size is it? seek-attr-rel-early ['size', 'right', 'rubber'] large
QUES 5 What about its material? seek-attr-imm ['material'] rubber
QUES 6 Does it have objects to behind itself in the image? exist-obj-rel-imm ['behind'] yes
QUES 7 How about to its right? exist-obj-rel-imm2 ['right'] yes
QUES 8 If there is an object to the right of the previous big object, what size is it? seek-attr-rel-early ['size', 'right', 'large'] large
