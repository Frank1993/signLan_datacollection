class FeatureExtractor(object):
    """docstring for FeatureExtractor"""
    def __init__(self):
        super(FeatureExtractor, self).__init__()

    def getFeature(self,frame,fingerCla = None):
        # number of hands

        frame_record = []

        numHands = len(frame.hands)
        #frame_record.append(numHands)

        for hand in frame.hands:
            handAttrs = self.getHandFeatures(hand)
            isRight = "Right" if hand.isRight else "left"
            handAttrs.insert(0,isRight)

            if not hand.is_valid:
                continue

            arm = hand.arm

            fingers = hand.fingers

            prefix = "RH" if hand.is_right else "LH" # right hand or left hand


            for finger in fingers:
                #print "finger:",finger.type
                #print '\n'

                is_extended = finger.is_extended
                #print "is_extended",is_extended
                #print "\n"
                if is_extended:
                    frame_record.append(1)
                else:
                    frame_record.append(0)

                finger_direction = finger.direction
                #print "finger_direction",finger_direction[0]
                #print "\n"
                for i in range(3):
                    frame_record.append(finger_direction[i])

                for bonetype in range(0,3):
                    #print "bone:",bonetype
                    #print "\n"
                    bone = finger.bone(bonetype)
                    bone_direction = bone.direction
                    for i in range(3):
                        frame_record.append(bone_direction[i])

                    #print "bone direction", bone_direction
        if fingerCla != None:
            frame_record.append(fingerCla)
        return frame_record

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
            return [finger.type, finger.is_extended,finger.direction,finger.length,finger.stabilized_tip_position,finger.tip_position, finger.tip_velocity,finger.touch_distance, finger.touch_zone]

    def getBoneFeatures(self, bone):
