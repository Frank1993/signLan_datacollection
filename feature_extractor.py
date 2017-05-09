class FeatureExtractor(object):
    """docstring for FeatureExtractor"""
    def __init__(self):
        super(FeatureExtractor, self).__init__()

    def getFeature(self,frame,fingerCla = None):
        # number of hands

        frame_record = []

        numHands = len(frame.hands)
        #frame_record.append(numHands)

        handsAttrsDict = {}

        for hand in frame.hands:
            isRight = 1 if hand.isRight else 0

            handAttrs = self.getHandFeatures(hand)

            arm = hand.arm
            armAttrs = self.getArmFeatures(arm)
            handAttrs.extend(armAttrs)

            fingers = hand.fingers
            fingersAttrsDict = {}
            for finger in fingers:
                if finger.is_valid:
                    fingersAttrsDict[finger.type] = self.getFingerFeatures(finger)

            fingersAttrs = []
            for i in range(0,5):
                if i in fingersAttrsDict:
                    fingersAttrs.extend(fingersAttrsDict[i])
                else:
                    fingersAttrs.extend([None] *(8 + 4*7))

            handAttrs.extend(fingersAttrs)

            handsAttrsDict[isRight] = handAttrs

        handsAttrs = []
        if 0 in handsAttrsDict:
            handsAttrs.extend(handsAttrsDict[0])
        else:
            handsAttrs.extend([None] * (12 + 5 + 5 * (8 + 4 * 7)))   # 12 for each hand, 5 for each arm, 8 for each finger, 7 for each none

        if 1 in handsAttrsDict:
            handsAttrs.extend(handsAttrsDict[1])
        else:
            handsAttrs.extend([None] *  (12 + 5 + 5 * (8 + 4 * 7)))


        return handsAttrs

    def getHandFeatures(self,hand):
        # <is_valid, confidence, basis, directions, palm_normal, palm_position, palm_velocity, palm_width, wrist_position, grab_strength, pinch_strength,sphere_center,sphere_radius>
        #assert hand.is_valid , "the hand should be valid to extract features"


        if hand.is_valid:
            return [hand.confidence, hand.basis, hand.directions, hand.palm_normal, hand.palm_position, hand.palm_velocity, hand.palm_width, hand.wrist_position,hand.grab_strength, hand.pinch_strength, hand.sphere_center, hand.sphere_radius]
        else:
            return [None] * 12

    def getArmFeatures(self,arm):
        if arm.is_valid:
            return [arm.basis,arm.direction, arm.elbow_position,arm.width,arm.wrist_position]
        else:
            return [None] * 5

    def getFingerFeatures(self,finger):
        # finger is a subclass of Pointables
        """
        tip_position: The tip position in millimeters from the Leap Motion origin.
        tip_velocity: The rate of change of the tip position in millimeters/second.
        direction: The direction in which this finger or tool is pointing. The direction is expressed as a unit vector pointing in the same direction as the tip.
        length: The estimated length of the finger or tool in millimeters.
        touch_zone: The current touch zone of this Pointable object. When a Pointable moves close to the adaptive touch plane, it enters the “hovering” zone. When a Pointable reaches or passes through the plane, it enters the “touching” zone.
        touch_distance: A value proportional to the distance between this Pointable object and the adaptive touch plane.
        type: 0 = TYPE_THUMB
              1 = TYPE_INDEX
              2 = TYPE_MIDDLE
              3 = TYPE_RING
              4 = TYPE_PINKY
        """

        if finger.is_valid:
            fingerAttrs =  [finger.is_extended,finger.direction,finger.length,finger.stabilized_tip_position,finger.tip_position, finger.tip_velocity,finger.touch_distance, finger.touch_zone]
            for i in range(4):
                bone = finger.bone(i)
                boneAttrs = self.getBoneFeatures(bone)
                fingerAttrs.extend(boneAttrs)
            return fingerAttrs
        else:
            return [None] * (8 + 4*7) # 8 for each finger, 7 for each bone

    def getBoneFeatures(self, bone):
        """
        all fingers contain 4 bones that make up the anatomy of the finger.
        Bones are orderd from base to tip, indexed from 0 to 3.
        Warning: the thumb does not have a base metacarpal bone and therefore contains a valid, zero length bone at that location
        
        next_joint: the position of the end of the bone cloeset to the finger tip
        prev_joint: the position of the end of the bone cloeset to the wrist


        """
        if Bone.is_valid:
            return [bone.basis, bone.center, bone.length, bone.direction, bone.width, bone.next_joint, bone.prev_joint]
        else:
            return [None] * 7

if __name__ == "__main__":
    from data_collection import Deserialization

    de = Deserialization('frameOf1.frame')
    frames = de.frames
    print(frames)
