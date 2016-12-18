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
            fingers = hand.fingers

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

        