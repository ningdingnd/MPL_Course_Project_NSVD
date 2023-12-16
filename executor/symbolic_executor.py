
import numpy as np
from copy import deepcopy


from executor.clevr_statics import COLORS, MATERIALS, SHAPES, SIZES
from executor.clevr_statics import ANSWER_CANDIDATES as ANSWER_CANDIDATES_CLEVR
from executor.clevr_statics import ATTRIBUTES_ALL as ATTRIBUTES_ALL_CLEVR

from utils import load_clevr_scenes


class SymbolicExecutorClevr(object):
    """Symbolic executor for clevr-dialog
    """
    def __init__(self, scenesPath):
        super(SymbolicExecutorClevr, self).__init__()
        self.functions = {}
        self.registerFunctions()
        self.uniqueObjFlag = False
        self.colors = COLORS
        self.materials = MATERIALS
        self.shapes = SHAPES
        self.sizes = SIZES
        self.answer_candidates = ANSWER_CANDIDATES_CLEVR
        self.attribute_all = ATTRIBUTES_ALL_CLEVR
        self.scenes = load_clevr_scenes(scenesPath)

    def reset(self, sceneIdx):
        """Resets the scene

        Args:
            sceneIdx: The index of the new scene
        """
        self.scene = self.scenes[sceneIdx]
        for _obj in self.scene:
            _obj["identifier"] = None
        # store previous objects in a list to better answer
        # xxx-imm, xxx-imm2, xxx-group and xxx-early questions.
        self.objs = []
        self.groups = []
        self.visited = []
        self.currentObj = None
        self.currentGrp = []
        self.uniqueObjFlag = False

    def registerFunctions(self):
        """Registers the available functions of the executor.
        """
        # Captions - extreme location
        self.functions["extreme-right"] = self.extremeRight
        self.functions["extreme-left"] = self.extremeLeft
        self.functions["extreme-behind"] = self.extremeBehind
        self.functions["extreme-front"] = self.extremeFront
        self.functions["extreme-center"] = self.extremeCenter

        # Captions - multiple objects
        self.functions["count-att"] = self.countAttributeCaption

        # Captions - object relations
        self.functions["obj-relation"] = self.objRelation

        # Captions - unique object
        self.functions["unique-obj"] = self.uniqueObject

        # Questions - Count
        self.functions["count-all"] = self.countAll
        self.functions["count-other"] = self.countOther
        self.functions["count-all-group"] = self.countAllGroup
        self.functions["count-attribute"] = self.countAttribute
        self.functions["count-attribute-group"] = self.countAttributeGroup
        self.functions["count-obj-rel-imm"] = self.countObjRelImm
        self.functions["count-obj-rel-imm2"] = self.countObjRelImm2
        self.functions["count-obj-rel-early"] = self.countObjRelEarly
        self.functions["count-obj-exclude-imm"] = self.countObjExcludeImm
        self.functions["count-obj-exclude-early"] = self.countObjExcludeEarly

        # Questions - Exist
        self.functions["exist-other"] = self.existOther
        self.functions["exist-attribute"] = self.existAttribute
        self.functions["exist-attribute-group"] = self.existAttributeGroup
        self.functions["exist-obj-rel-imm"] = self.existObjRelImm
        self.functions["exist-obj-rel-imm2"] = self.existObjRelImm
        self.functions["exist-obj-rel-early"] = self.existObjRelEarly
        self.functions["exist-obj-exclude-imm"] = self.existObjExcludeImm
        self.functions["exist-obj-exclude-early"] = self.existObjExcludeEarly

        # Questions - Seek
        self.functions["seek-attr-imm"] = self.seekAttrImm
        self.functions["seek-attr-imm2"] = self.seekAttrImm
        self.functions["seek-attr-early"] = self.seekAttributeEarly
        self.functions["seek-attr-rel-imm"] = self.seekAttributeRelImm
        self.functions["seek-attr-rel-early"] = self.seekAttributeRelEarly


    ########################################################
    #                   Helper functions                   #
    ########################################################
    def getAttributeType(self, attribute):
        assert attribute in self.attribute_all, "The attribute {} is unkown".format(
            attribute)
        if attribute in self.colors:
            return "color"
        elif attribute in self.materials:
            return "material"
        elif attribute in self.shapes:
            return "shape"
        elif attribute in self.sizes:
            return "size"
        
    def filterAttribute(self, scene, attribute):
        attributeType = self.getAttributeType(attribute)
        filtered = []
        if len(scene) == 0:
            return filtered

        for _obj in scene:
            if _obj[attributeType] == attribute:
                filtered.append(_obj)
        return filtered

    def excludeAttribute(self, scene, obj, attributeType):
        filtered = []
        if len(scene) == 0:
            return filtered
        for _obj in scene:
            if _obj["id"] != obj["id"] and obj[attributeType] == _obj[attributeType]:
                filtered.append(_obj)

        # Update the visited objects list
        if len(filtered) > 0:
            for _obj in filtered:
                self.updateVisited(_obj)
        return filtered

    def execute(self, functionLabel, functionArgs):
        assert functionLabel in self.functions, "{} is not a valid function".format(
            functionLabel)
        function = self.functions[functionLabel]
        answer = function(*functionArgs)
        return answer

    def updateCurrentObj(self, obj):
        self.currentObj = obj
        objsCopy = deepcopy(self.objs)
        for i, _obj in enumerate(objsCopy):
            if _obj["id"] == obj["id"]:
                del self.objs[i]
        # Current obj is always kept at the end of the visited objs
        self.objs.append(obj)

    def updateVisited(self, obj):
        if len(self.visited) == 0:
            self.visited.append(obj)
        else:
            newObjFlag = True
            for _obj in self.visited:
                if _obj["id"] == obj["id"]:
                    newObjFlag = False
                    break
            if newObjFlag:
                self.visited.append(obj)

    def getOther(self):
        others = []
        if len(self.visited) < len(self.scene):
            for _obj in self.scene:
                notExisting = True
                for __obj in self.visited:
                    if __obj["id"] == _obj["id"]:
                        notExisting = False
                        break
                if notExisting:
                    others.append(_obj)
        return others

    def updateIdentifier(self, obj, attribute):
        if obj["identifier"] is None:
            obj["identifier"] = attribute
        else:
            identifiers = obj["identifier"].split("-")
            if attribute not in identifiers:
                identifiers.append(attribute)
                obj["identifier"] = "-".join(identifiers)


    ########################################################
    #                   Caption programs                   #
    ########################################################

    def extremeRight(self, *attributes):
        attributes = list(attributes)
        attributeTypes = list(
            map(lambda att: self.getAttributeType(att), attributes))

        leftToRight = deepcopy(self.scene)
        leftToRight.sort(key=lambda o: o["position"][0])
        extremeRightObj = leftToRight[-1]
        for attributeType, attribute in zip(attributeTypes, attributes):
            assert extremeRightObj[attributeType] == attribute
            self.updateIdentifier(extremeRightObj, attribute)

        self.updateCurrentObj(extremeRightObj)
        self.updateVisited(extremeRightObj)
        del leftToRight

    def extremeLeft(self, *attributes):
        attributes = list(attributes)
        attributeTypes = list(
            map(lambda att: self.getAttributeType(att), attributes))

        leftToRight = deepcopy(self.scene)
        leftToRight.sort(key=lambda o: o["position"][0])
        extremeLeftObj = leftToRight[0]
        for attributeType, attribute in zip(attributeTypes, attributes):
            assert extremeLeftObj[attributeType] == attribute
            self.updateIdentifier(extremeLeftObj, attribute)

        self.updateCurrentObj(extremeLeftObj)
        self.updateVisited(extremeLeftObj)
        del leftToRight

    # TODO: Re-implement this function 
    def extremeFront(self, *attributes):
        raise NotImplementedError

    # TODO: Re-implement this function 
    def extremeBehind(self, *attributes):
        raise NotImplementedError

    def extremeCenter(self, *attributes):
        attributes = list(attributes)
        attributeTypes = list(
            map(lambda att: self.getAttributeType(att), attributes))
        numObjs = len(self.scene)

        frontToBack = deepcopy(self.scene)
        frontToBack.sort(key=lambda o: o["position"][1], reverse=True)

        rightToLeft = deepcopy(self.scene)
        rightToLeft.sort(key=lambda o: o["position"][0], reverse=True)

        prelimenaryCandidates = []

        for i, objFrontToBack in enumerate(frontToBack):
            numObjsInFront = i
            numObjsBehind = len(rightToLeft) - i - 1
            if numObjsInFront <= numObjs / 2 and numObjsBehind <= numObjs / 2:
                prelimenaryCandidates.append(objFrontToBack)
        foundCenter = False
        for _obj in prelimenaryCandidates:
            for i, objRightToLeft in enumerate(rightToLeft):
                if _obj["id"] == objRightToLeft["id"]:
                    numObjsToTheRight = i
                    numObjsToTheLeft = len(frontToBack) - i - 1
                    if numObjsToTheRight <= numObjs / 2 and numObjsToTheLeft <= numObjs / 2:
                        foundCenter = True
                        for attributeType, attribute in zip(attributeTypes, attributes):
                            if _obj[attributeType] != attribute:
                                foundCenter = False
                                break
                        break
            if foundCenter:
                break
        for attributeType, attribute in zip(attributeTypes, attributes):
            self.updateIdentifier(_obj, attribute)
        self.updateCurrentObj(_obj)
        self.updateVisited(_obj)
        del rightToLeft, frontToBack

    # TODO: Re-implement this function 
    def countAttributeCaption(self, attribute):
        raise NotImplementedError

    def getAnchorAttribute(self, attribute_1, attribute_2, scene):
        # The anchor object is unique. If we filter the object list
        # based on the attribute anchor, we must find only one object.
        filterAttribute_1 = self.filterAttribute(scene, attribute_1)
        if len(filterAttribute_1) == 1:
            return attribute_1
        else:
            return attribute_2

    def objRelation(self, attribute, attributeAnchor, relation):
        assert relation in ["left", "right", "front", "behind"]
        # find the anchor object
        if attributeAnchor != self.getAnchorAttribute(attribute, attributeAnchor, self.scene):
            temp = deepcopy(attribute)
            attribute = deepcopy(attributeAnchor)
            attributeAnchor = temp
            if relation == "left":
                relation = "right"
            elif relation == "right":
                relation = "left"
            elif relation == "behind":
                relation = "front"
            elif relation == "front":
                relation = "behind"

        # Order the objects in the scene w.r.t. the relation
        sceneCopy = deepcopy(self.scene)

        if relation in ["left", "right"]:
            sceneCopy.sort(key=lambda o: o["position"][0])
        else:
            sceneCopy.sort(key=lambda o: o["position"][1])

        # get the anchor object
        attributeTypeAnchor = self.getAttributeType(attributeAnchor)
        for i, _obj in enumerate(sceneCopy):
            if _obj[attributeTypeAnchor] == attributeAnchor:
                break
        # save the anchor object before the main object
        anchorObj = _obj
        self.updateIdentifier(anchorObj, attributeAnchor)
        self.updateCurrentObj(anchorObj)
        self.updateVisited(anchorObj)

        if relation in ["left", "behind"]:
            sceneCopy = list(reversed(sceneCopy[:i]))
        else:
            sceneCopy = sceneCopy[i+1:]

        attributeType = self.getAttributeType(attribute)
        # get the main object
        for _obj in sceneCopy:
            # and not equalDicts(_obj, anchorObj):
            if _obj[attributeType] == attribute:
                break
        self.updateIdentifier(_obj, attribute)
        self.updateCurrentObj(_obj)
        self.updateVisited(_obj)
        del sceneCopy

    # TODO: Re-implement this function 
    def uniqueObject(self, *attributes):
        raise NotImplementedError

    ########################################################
    #                  Question programs                   #
    ########################################################
    def filterLeft(self, scene, obj):
        filtered = []
        if len(scene) == 0:
            return filtered

        for _obj in self.scene:
            # if the x-coordinate of _obj is smaller than the x-coordinate of slef.currentObj,
            # then _obj is located to the left of self.currentObj
            if _obj["position"][0] < obj["position"][0] and _obj["id"] != obj["id"]:
                filtered.append(_obj)
        return filtered

    # TODO: Re-implement this function 
    def filterRight(self, scene, obj):
        raise NotImplementedError

    # TODO: Re-implement this function 
    def filterFront(self, scene, obj):
        raise NotImplementedError

    # TODO: Re-implement this function 
    def filterBehind(self, scene, obj):
        raise NotImplementedError

    def filterPosition(self, scene, obj, pos):
        assert pos in ["left", "right", "front", "behind"]
        if pos == "left":
            filtered = self.filterLeft(scene, obj)
        elif pos == "right":
            filtered = self.filterRight(scene, obj)
        elif pos == "front":
            filtered = self.filterFront(scene, obj)
        elif pos == "behind":
            filtered = self.filterBehind(scene, obj)
        return filtered

    ###########################################################################
    #                           Counting questions                            #
    ###########################################################################
    def countAll(self):
        self.currentGrp = deepcopy(self.scene)
        self.groups.append(deepcopy(self.scene))
        return len(self.scene)

    def countOther(self):
        others = self.getOther()
        if len(others) > 0:
            self.currentGrp = others
            self.groups.append(others)
        if len(others) == 1:
            obj = others[0]
            for _obj in self.objs:
                if _obj["id"] == obj["id"]:
                    obj = _obj
                    break
            self.updateCurrentObj(obj)

            self.updateVisited(obj)
        return len(others)

    def countAllGroup(self):
        return len(self.currentGrp)

    # TODO: Re-implement this function 
    def countAttribute(self, attribute, updateCurrentObj=True):
        raise NotImplementedError

    # TODO: Re-implement this function 
    def countAttributeGroup(self, attribute, updateCurrentObj=True):
        raise NotImplementedError

    def countObjRelImm(self, pos, updateCurrentObj=True):
        filtered = self.filterPosition(self.scene, self.currentObj, pos)
        if len(filtered) == 0:
            return 0
        # Update the visited objects list
        for _obj in filtered:
            self.updateVisited(_obj)

        self.currentGrp = filtered
        self.groups.append(filtered)

        if len(filtered) == 1:
            obj = filtered[0]
            new = True
            for _obj in self.objs:
                if _obj["id"] == obj["id"]:
                    obj = _obj
                    new = False
                    break
            if updateCurrentObj:
                self.updateCurrentObj(obj)
                self.uniqueObjFlag = True
            else:
                if new:
                    self.objs.append(obj)
        return len(filtered)

    def countObjRelImm2(self, pos):
        if self.uniqueObjFlag:
            # del self.objs[-1]
            self.updateCurrentObj(self.objs[-2])
            self.uniqueObjFlag = False
        return self.countObjRelImm(pos)

    # TODO: Re-implement this function 
    def countObjRelEarly(self, pos, earlyObjAttribute, updateCurrentObj=True):
        raise NotImplementedError

    def countObjExcludeImm(self, attributeType, updateCurrentObj=True):
        filtered = self.excludeAttribute(
            self.scene, self.currentObj, attributeType)
        if len(filtered) == 0:
            return 0

        if len(filtered) == 1:
            obj = filtered[0]
            new = True
            for _obj in self.objs:
                if _obj["id"] == obj["id"]:
                    obj = _obj
                    new = False
                    break
            if updateCurrentObj:
                self.updateCurrentObj(obj)
            else:
                if new:
                    self.objs.append(obj)

        self.currentGrp = filtered
        self.groups.append(filtered)
        return len(filtered)

    # TODO: Re-implement this function 
    def countObjExcludeEarly(self, attributeType, earlyObjAttribute, updateCurrentObj=True):
        raise NotImplementedError

    ###########################################################################
    #                           Existence questions                           #
    ###########################################################################

    def existOther(self):
        others = self.getOther()
        numOther = len(others)
        if numOther > 0:
            self.currentGrp = others
            self.groups.append(others)
            for _obj in others:
                self.updateVisited(_obj)
        return "yes" if numOther > 0 else "no"

    # TODO: Re-implement this function 
    def existAttribute(self, attribute):
        raise NotADirectoryError

    def existAttributeGroup(self, attribute):
        numAttributeGrp = self.countAttributeGroup(
            attribute, updateCurrentObj=False)
        return "yes" if numAttributeGrp > 0 else "no"

    # TODO: Re-implement this function 
    def existObjRelImm(self, pos):
        raise NotImplementedError

    def existObjRelEarly(self, pos, earlyObjAttribute):
        numObjs = self.countObjRelEarly(
            pos, earlyObjAttribute, updateCurrentObj=False)
        return "yes" if numObjs > 0 else "no"

    def existObjExcludeImm(self, attributeType):
        numObjs = self.countObjExcludeImm(
            attributeType, updateCurrentObj=False)
        return "yes" if numObjs > 0 else "no"

    # TODO: Re-implement this function 
    def existObjExcludeEarly(self, attributeType, earlyObjAttribute):
        raise NotImplementedError

    ###########################################################################
    #                             Seek questions                              #
    ###########################################################################

    def seekAttrImm(self, attributeType):
        assert attributeType in self.currentObj, "Attributre <{}> is not valid"
        self.updateIdentifier(self.currentObj, self.currentObj[attributeType])
        return self.currentObj[attributeType]

    # TODO: Re-implement this function 
    def seekAttributeEarly(self, attributeType, earlyObjAttribute):
        raise NotImplementedError

    def seekAttributeRelImm(self, attributeType, pos):
        filtered = self.filterPosition(self.scene, self.currentObj, pos)
        if len(filtered) == 0:
            return "none"
        else:
            # Get the closest object to slef.obj
            if pos == "left":
                filtered.sort(key=lambda x: x["position"][0])
                obj = filtered[-1]
            elif pos == "right":
                filtered.sort(key=lambda x: x["position"][0])
                obj = filtered[0]
            elif pos == "front":
                filtered.sort(key=lambda x: x["position"][1])
                obj = filtered[0]
            elif pos == "behind":
                filtered.sort(key=lambda x: x["position"][1])
                obj = filtered[-1]

            for _obj in self.objs:
                if _obj["id"] == obj["id"]:
                    obj["identifier"] = _obj["identifier"]
                    break
            self.updateIdentifier(obj, obj[attributeType])
            self.updateCurrentObj(obj)
            self.updateVisited(obj)
            return obj[attributeType]

    # TODO: Re-implement this function 
    def seekAttributeRelEarly(self, attributeType, pos, earlyObjAttribute):
        raise NotImplementedError


