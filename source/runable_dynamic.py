# -*- coding:utf-8 -*-
import sys
sys.path.append("../LeapMotionSDK")
import Leap
#import sys
#import ctypes,numpy
#import matplotlib

#from PIL import Image
#from model import getClf

#from feature_extractor import FeatureExtractor
import numpy as np
from DataAgent import convertFramesToFeatures
from signPredictor import predict

class SampleListener(Leap.Listener):
    """
    def __init__(self,serialize_file):
        super.__init__()
        self.serialize_stream = open(serialize_file,'wb')
    """
    def on_connect(self, controller):
        print("Connected")


    def on_frame(self, controller):
        # get a frame
        frame = controller.frame()
        if not frame.hands.is_empty:
              #print("On Frame")
              self.isCollectingFrames = True
              self.frames.append(frame)
        elif self.isCollectingFrames == True:
            self.isCollectingFrames = False

            frames = self.frames[10:-10:10]
            features = convertFramesToFeatures(frames)
            predict_result = predict(features)
            print(predict_result)
            self.frames = []




def main():
    # Create a sample listener and controller

    frames = []
    listener = SampleListener()
    listener.frames = frames
    listener.isCollectingFrames = False

    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_IMAGES)

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    

    # Keep this process running until Enter is pressed
    print( "Press Enter to quit...")
    try:

        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        sess.close()
        print("Thank you for your using!")

if __name__ == "__main__":
    main()