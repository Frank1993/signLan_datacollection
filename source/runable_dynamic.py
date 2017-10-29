# -*- coding:utf-8 -*-
import sys
sys.path.append("../LeapMotionSDK")
import Leap

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication
#import sys
import ctypes,numpy
#import matplotlib

from PIL import Image
from PIL.ImageQt import ImageQt
#from model import getClf

#from feature_extractor import FeatureExtractor
import numpy as np
from DataAgent import convertFramesToFeatures
from signPredictor import predict
from Main_window import MainWindow


from model import getClf

from feature_extractor import FeatureExtractor

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
        
        feature = np.array([feature]).reshape(1,-1)
        predicted = self.model.predict(feature)
        #print predicted
        self.isClassifying = False
        

        return predicted[0]
        """
        else:
            self.isClassifying = False
            return "Please put one your fingers"
        """

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

        if not self.window.isCollectingData:
            image = controller.images[1]
            if image.is_valid:
                address = int(image.data_pointer)
                ctype_array_def = ctypes.c_ubyte * image.width * image.height
                as_ctype_array = ctype_array_def.from_address(address)
                as_numpy_array = numpy.ctypeslib.as_array(as_ctype_array)
                buffers = numpy.reshape(as_numpy_array,(image.height,image.width))
                pil_image = Image.fromarray(buffers,"L")
                pil_image = pil_image.convert("RGB")
                qtImage = ImageQt(pil_image)
                self.window.setNewImage(qtImage)

        if not frame.hands.is_empty:
              #print("On Frame")
              self.isCollectingFrames = True
              self.frames.append(frame)
        elif self.isCollectingFrames == True:
            self.isCollectingFrames = False

            if self.window.isCollectingData:
                self.window.persisitData(self.frames)
                self.frames = []
            else:
                if self.window.isPredictingDynamic:
                    frames = self.frames[10:-10:10]
                    features = convertFramesToFeatures(frames)
                    predict_result = predict(features)
                    #("we",0),("hello",1),("you",2),("teacher",3),("no",4),("eat",5)
                    label_info = {0:"们",1:"好",2:"你",3:"老师",4:"不",5:"吃饭"}
                    print(label_info[predict_result])
                    self.window.setPredictedLabel(label_info[predict_result])
                    self.frames = []
                else:
                    frame = self.frames[len(self.frames)/2]
                    if not self.classifier.isClassifying:
                        label = str(1 + self.classifier.predict(frame))
                        print "Sign：",
                        self.window.setPredictedLabel(label)
                    self.frames = []
    """
    def on_images(self,controller):
        if not self.window.isCollectingData:
            image = controller.images[1]
            if image.is_valid:
                address = int(image.data_pointer)
                ctype_array_def = ctypes.c_ubyte * image.width * image.height
                as_ctype_array = ctype_array_def.from_address(address)
                as_numpy_array = numpy.ctypeslib.as_array(as_ctype_array)
                buffers = numpy.reshape(as_numpy_array,(image.height,image.width))
                pil_image = Image.fromarray(buffers,"L")
                pil_image = pil_image.convert("RGB")
                qtImage = ImageQt(pil_image)
                self.window.setNewImage(qtImage)
    """


def main():
    # Create a sample listener and controller
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()

    frames = []
    listener = SampleListener()
    listener.classifier = Classifier()
    listener.frames = frames
    listener.isCollectingFrames = False
    listener.window = win

    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_IMAGES)

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    
    sys.exit(app.exec_())
    dataSe = DataSerialization(frames,serialize_stream)

    serialize_stream.close()
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