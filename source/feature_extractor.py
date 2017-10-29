import os

filepath = os.path.realpath(__file__)
projectDir = os.path.dirname(os.path.dirname(filepath))

leapMotionSDKPath = os.path.join(projectDir, "LeapMotionSDK")

import sys
sys.path.append(leapMotionSDKPath)

import Leap

class AttributeFilter(object):
    @classmethod
    def handRule(cls):
        """
        features of hand:
        hand.confidence: float
        hand.basis.x_basis: vector, 3-dim
        hand.basis.y_basis: vector
        hand.basis.z_basis: vector
        hand.direction: vector
        hand.palm_normal: vector
        hand.palm_position: vector
        hand.palm_velocity: vector
        hand.width: float
        hand.wrist_position: vector
        hand.grab_strength: float
        hand.pinch_strength: float
        hand.sphere_center: vector
        hand.sphere_radius: float
        """
        return [("hand_confidence","float",False,False),
                ("hand_basis_xbasis","vector",False,True),
                ("hand_basis_ybasis","vector",False,True),
                ("hand_basis_zbasis","vector",False,True),
                ("hand_direction","vector",True,True),
                ("hand_palm_normal","vector",True,True),
                ("hand_palm_position","vector",False,True),
                ("hand_palm_velocity", "vector", False, True),
                ("hand_width","float",False,True), 
                ("hand_wrisit_position","vector",False,True),
                ("hand_grab_strength","float",False,True),
                ("hand_pinch_strength","float",False,True),
                ("hand_sphere_center","vector",False,True),
                ("hand_sphere_radius","float",False,True)]

    @classmethod
    def armRule(cls):
        """
        arm.basis.x_basis: vector
        arm.basis.y_basis: vector
        arm.basis.z_basis: vector
        arm.direction: vector 
        arm.elbow_position: vector
        arm.width: float
        arm.wrist_position: vector 
        """
        return [("arm_basis_xbasis","vector",False,True),
                ("arm_basis_ybasis","vector",False,True),
                ("arm_basis_zbasis","vector",False,True),
                ("arm_direction","vector",False,True),
                ("arm_elbow_position","vector",False,True),
                ("arm_width","float",False,True),
                ("arm_wrist_position","vector",False,True)]
    @classmethod
    def fingerRule(cls):
        """
        finger.is_extended: float
        finger.direction: vector
        finger.length: float
        finger.stabilized_tip_position: vector
        finger.tip_position: vector
        finger.tip_velocity: vector
        finger.touch_distance: float
        finger.touch_zone: integer
        """
        return [("finger_is_extended","float",True,False),
                ("finger_direction","vector",True,True),
                ("finger_length","float",False,True),
                ("finger_stabilized_tip_position","vector",False,True),
                ("finger_tip_position","vector",False,True),
                ("finger_tip_velocity","vector",False,True),
                ("finger_touch_distance","float",False,True),
                ("finger_touch_zone","float",False,False)]

    @classmethod
    def boneRule(cls):
        """
        bone.basis.x_basis: vector
        bone.basis.y_basis: vector
        bone.basis.z_basis: vector
        bone.center: vector
        bone.length: float
        bone.direction: vector
        bone.width: float
        bone.next_joint: vector
        bone.prev_joint vector 
        """
        return [("bone_basis_xbasis","vector",False,True),
                ("bone_basis_ybasis","vector",False,True),
                ("bone_basis_zbasis","vector",False,True),
                ("bone_center","vector",False,True),
                ("bone_length","float",False,True),
                ("bone_direction","vector",False,True),
                ("bone_width","float",False,True),
                ("bone_next_joint","vector",False,True),
                ("bone_prev_joint","vector",False,True)]

    @classmethod
    def filter(cls, attrs,rule):
        assert len(attrs) == len(rule), "the length of attributes and filter rules should be consistent"
        filterdAttrs = []
        for i in range(len(attrs)):
            if rule[i][2] == True:
                filterdAttrs.append(attrs[i])
        return filterdAttrs

    @classmethod
    def filterHand(cls,attrs):
        handRl = cls.handRule()
        return cls.filter(attrs,handRl)

    @classmethod
    def filterArm(cls,attrs):
        armRl = cls.armRule()
        return cls.filter(attrs,armRl)

    @classmethod
    def filterFinger(cls,attrs):
        fingerRl = cls.fingerRule()
        return cls.filter(attrs,fingerRl)

    @classmethod
    def filterBone(cls,attrs):
        boneRl = cls.boneRule()
        return cls.filter(attrs,boneRl)

    @classmethod
    def featureNum(cls,rule):
        num = 0
        for r in rule:
            if r[2] == True:
                if r[1] == "float":
                    num += 1
                else:
                    num += 3

        return num

    @classmethod
    def handFeatureNum(cls):
        handRl = cls.handRule()
        return cls.featureNum(handRl)

    @classmethod
    def armFeatureNum(cls):
        armRl = cls.armRule()
        return cls.featureNum(armRl)

    @classmethod
    def fingerFeatureNum(cls):
        fingerRl = cls.fingerRule()
        return cls.featureNum(fingerRl)

    @classmethod
    def boneFeatureNum(cls):
        boneRl = cls.boneRule()
        return cls.featureNum(boneRl)



    @classmethod
    def expandAttrsName(cls,attrs,attrsType,prefix):
        if attrsType == "float":
            return [prefix+attrs]

        return [prefix + attrs+"_x",prefix + attrs+"_y",prefix + attrs+"_z"]

    @classmethod
    def featureName(cls,rule,prefix):
        name = []
        for r in rule:
            if r[2] == True:
                name.extend(cls.expandAttrsName(r[0],r[1],prefix))
        return name
        
    @classmethod
    def frameFeatureName(cls):
        frameFeatureNames = []
        for handType in ["right_"]:
            handFeatureName = []
            handFeatureName.extend(cls.featureName(cls.handRule(),handType))
            handFeatureName.extend(cls.featureName(cls.armRule(),handType))
            for fingerType in ["THUMB_","INDEX_","MIDDLE_","RING_","PINKY_"]:
                fingerName = cls.featureName(cls.fingerRule(),handType + fingerType)
                for boneType in ["0_","1_","2_","3_"]:
                    boneName = cls.featureName(cls.boneRule(),handType + fingerType + boneType)
                    fingerName.extend(boneName)
                handFeatureName.extend(fingerName)

            frameFeatureNames.extend(handFeatureName)

        return frameFeatureNames

    @classmethod
    def getDuplicateIndexes(cls):
        indicator = []
        for handType in ["right_"]:
            indicator.extend(cls.getOscilateIndexes(cls.handRule()))
            indicator.extend(cls.getOscilateIndexes(cls.armRule()))
            for i in range(5):
                fingerInd = cls.getOscilateIndexes(cls.fingerRule())
                for i in range(4):
                    fingerInd.extend(cls.getOscilateIndexes(cls.boneRule()))
                indicator.extend(fingerInd)
        return indicator
    @classmethod
    def getOscilateIndexes(cls,rules):
        indicator = []
        for rule in rules:
            if rule[2]:
                if rule[1] == "float":
                    indicator.extend([rule[3]])
                else:
                    for i in range(3):
                        indicator.extend([rule[3]])
        return indicator







class FeatureExtractor(object):
    """docstring for FeatureExtractor"""
    def __init__(self):
        super(FeatureExtractor, self).__init__()

    def getFeature(self,frame,fingerCla = None):
    # number of hands

        frame_record = []


        handsAttrsDict = {}

        for hand in frame.hands:
            isRight = 1 if hand.is_right else 0

            handFeatures = self.getHandFeatures(hand)

            arm = hand.arm
            armFeatures = self.getArmFeatures(arm)
            handFeatures.extend(armFeatures)

            fingers = hand.fingers
            fingersAttrsDict = {}
            for finger in fingers:
                if finger.is_valid:
                    fingersAttrsDict[finger.type] = self.getFingerFeatures(finger)

            fingerFeatures = []
            for i in range(0,5):
                if i in fingersAttrsDict:
                    fingerFeatures.extend(fingersAttrsDict[i])
                else:
                    fingerFeatures.extend( [0.0] * (AttributeFilter.fingerFeatureNum() + 4 *AttributeFilter.boneFeatureNum()) )

            handFeatures.extend(fingerFeatures)

            handsAttrsDict[isRight] = handFeatures

        handsFeatures= []
        #if 0 in handsAttrsDict:
            #handsFeatures.extend(handsAttrsDict[0])
        #else:
            #handsFeatures.extend([0.0] * (AttributeFilter.handFeatureNum() + AttributeFilter.armFeatureNum() + 5 * (AttributeFilter.fingerFeatureNum() + 4 *AttributeFilter.boneFeatureNum())) )   # (5 + 3*9) for each hand, (1 + 3 * 6) for each arm, 8 for each finger, 7 for each none

        if 1 in handsAttrsDict:
            handsFeatures.extend(handsAttrsDict[1])
        else:
            handsFeatures.extend([0.0] *  (AttributeFilter.handFeatureNum() + AttributeFilter.armFeatureNum() + 5 * (AttributeFilter.fingerFeatureNum() + 4 *AttributeFilter.boneFeatureNum())) )

        if fingerCla != None:
            handsFeatures.append(fingerCla)
        return handsFeatures

    def attrsToFeatures(self,attrs):
        features = []
        for attr in attrs:
            if type(attr)== float or type(attr) == int:
                features.append(attr)
            elif type(attr) == Leap.Vector:
                features.append(attr[0])
                features.append(attr[1])
                features.append(attr[2])
            else:
                print "bad attrs:" + type(attr)

        return features
    def getHandFeatures(self,hand):
        """
        features of hand:
        hand.confidence: float
        hand.basis.x_basis: vector, 3-dim
        hand.basis.y_basis: vector
        hand.basis.z_basis: vector
        hand.direction: vector
        hand.palm_normal: vector
        hand.palm_position: vector
        hand.palm_velocity: vector
        hand.width: float
        hand.wrist_position: vector
        hand.grab_strength: float
        hand.pinch_strength: float
        hand.sphere_center: vector
        hand.sphere_radius: float
        """

        if hand.is_valid:
            handAttrs =  [hand.confidence, hand.basis.x_basis,hand.basis.y_basis,hand.basis.z_basis, hand.direction, hand.palm_normal, hand.palm_position, hand.palm_velocity, hand.palm_width, hand.wrist_position,hand.grab_strength, hand.pinch_strength, hand.sphere_center, hand.sphere_radius]
            handAttrs = AttributeFilter.filterHand(handAttrs)
            handFeatures  = self.attrsToFeatures(handAttrs)

            assert len(handFeatures) == AttributeFilter.handFeatureNum() , "length of hand features not consistent"
            return handFeatures
        else:
            return [None] * AttributeFilter.handFeatureNum() # 5 float and 9 vector

    def getArmFeatures(self,arm):
        """
        arm.basis.x_basis: vector
        arm.basis.y_basis: vector
        arm.basis.z_basis: vector
        arm.direction: vector 
        arm.elbow_position: vector
        arm.width: float
        arm.wrist_position: vector
        """
        if arm.is_valid:
            armAttrs =  [arm.basis.x_basis,arm.basis.y_basis,arm.basis.z_basis,arm.direction, arm.elbow_position,arm.width,arm.wrist_position]
            armAttrs = AttributeFilter.filterArm(armAttrs)
            armFeatures = self.attrsToFeatures(armAttrs)
            assert len(armFeatures) == AttributeFilter.armFeatureNum(), "length of arm features not consistent"
            return armFeatures
        else:
            return [None] * AttributeFilter.armFeatureNum() # one float and 6 vector

    def getFingerFeatures(self,finger):
        # finger is a subclass of Pointables
        """
        tip_position: The tip position in millimeters from the Leap Motion origin.
        tip_velocity: The rate of change of the tip position in millimeters/second.
        direction: The direction in which this finger or tool is pointing. The direction is expressed as a unit vector pointing in the same direction as the tip.
        length: The estimated length of the finger or tool in millimeters.
        touch_zone: The current touch zone of this Pointable object. When a Pointable moves close to the adaptive touch plane, it enters the "hovering" zone. When a Pointable reaches or passes through the plane, it enters the "touching" zone.
        touch_distance: A value proportional to the distance between this Pointable object and the adaptive touch plane.
        type: 0 = TYPE_THUMB
              1 = TYPE_INDEX
              2 = TYPE_MIDDLE
              3 = TYPE_RING
              4 = TYPE_PINKY


        features of finger
        finger.is_extended: int
        finger.direction: vector
        finger.length: float
        finger.stabilized_tip_position: vector
        finger.tip_position: vector
        finger.tip_velocity: vector
        finger.touch_distance: float
        finger.touch_zone: integer
        
        4 + 3 * 4 ### 4 float and 4 vector for only finger not include bone

        """

        if finger.is_valid:
            fingerAttrs =  [1.0 if finger.is_extended else 0.0,finger.direction,finger.length,finger.stabilized_tip_position,finger.tip_position, finger.tip_velocity,finger.touch_distance, finger.touch_zone]
            fingerAttrs = AttributeFilter.filterFinger(fingerAttrs)
            fingerFeatures = self.attrsToFeatures(fingerAttrs)
            for i in range(4):
                bone = finger.bone(i)
                boneFeatures = self.getBoneFeatures(bone)
                fingerFeatures.extend(boneFeatures)

            assert len(fingerFeatures) == (AttributeFilter.fingerFeatureNum() + 4 *AttributeFilter.boneFeatureNum()), "length of finger features not consistent"
            return fingerFeatures
        else:
            return [None] *  (AttributeFilter.fingerFeatureNum() + 4 *AttributeFilter.boneFeatureNum()) # (4 + 3 * 4) for each finger, (2 + 3*7) for each bone

    def getBoneFeatures(self, bone):
        """
        all fingers contain 4 bones that make up the anatomy of the finger.
        Bones are orderd from base to tip, indexed from 0 to 3.
        Warning: the thumb does not have a base metacarpal bone and therefore contains a valid, zero length bone at that location
        
        next_joint: the position of the end of the bone cloeset to the finger tip
        prev_joint: the position of the end of the bone cloeset to the wrist
        
        feature of bone:
        bone.basis.x_basis: vector
        bone.basis.y_basis: vector
        bone.basis.z_basis: vector
        bone.center: vector
        bone.length: float
        bone.direction: vector
        bone.width: float
        bone.next_joint: vector
        bone.prev_joint vector 


        """
        if bone.is_valid:
            boneAttrs =  [bone.basis.x_basis,bone.basis.y_basis,bone.basis.z_basis, bone.center, bone.length, bone.direction, bone.width, bone.next_joint, bone.prev_joint]
            boneAttrs = AttributeFilter.filterBone(boneAttrs)
            boneFeatures = self.attrsToFeatures(boneAttrs)

            assert len(boneFeatures) == AttributeFilter.boneFeatureNum(), "length of bone features not consistent"
            return boneFeatures
        else:
            return [None] * AttributeFilter.boneFeatureNum() # 2 float and 7 vector

if __name__ == "__main__":
    from data_collection import Deserialization

    de = Deserialization(os.path.join(projectDir,"frameOf1.frame"))
    frames = de.frames
    
    testFrame = frames[100]
    featureExtactor = FeatureExtractor()

    features = featureExtactor.getFeature(testFrame)
    #print(features)
    print(len(features))

    featureName= AttributeFilter.frameFeatureName()
    #print(featureName)
    print(len(featureName))

    duplicateIndexes =  AttributeFilter.getDuplicateIndexes()
    #print duplicateIndexes
    print len(duplicateIndexes)
    print len(duplicateIndexes) - sum(duplicateIndexes)
    
