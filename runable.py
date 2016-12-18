# -*- coding:utf-8 -*-
import Leap
import sys
import ctypes,numpy
import matplotlib

from PIL import Image
from model import getClf

from feature_extractor import FeatureExtractor
import numpy as np
class Classifier(object):
    """docstring for Classifier"""
    
    def __init__(self):
        super(Classifier, self).__init__()
        self.model = getClf()
        self.feature_extractor = FeatureExtractor()
        self.isClassifying = False
    def predict(self,frame):
        self.isClassifying = True
        feature = self.feature_extractor.getFeature(frame)
        if len(feature) == 65:
            feature = np.array([feature]).reshape(1,-1)
            predicted = self.model.predict(feature)
            #print predicted
            self.isClassifying = False

            if predicted[0] == 0:
                return "1"
            else:
                return "2"
        else:
            self.isClassifying = False
            return "请放上手指"


class SampleListener(Leap.Listener):

    def on_connect(self, controller):
        print "Connected"


    def on_frame(self, controller):
        #print "Frame available"
        frame = controller.frame()

        if not self.classifier.isClassifying:
            print "手势：",self.classifier.predict(frame)
 

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    listener.classifier = Classifier()

    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_IMAGES)

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
