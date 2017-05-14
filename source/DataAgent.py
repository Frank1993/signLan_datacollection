from feature_extractor import AttributeFilter, FeatureExtractor
from data_collection import Deserialization

import os

def getFeatureAndLabel():

    dynamicDataPath = os.path.abspath("../DynamicData")

    features = []
    labels = []
    featureExtactor = FeatureExtractor()
    for motion in ["we","WeHello"]:
        for i in range(1,51):
            leapFile = os.path.join(dynamicDataPath,"%s%s.lp"%(motion,i))
            de = Deserialization(leapFile)
            frames = de.frames
            frameFeature = []
            for frame in frames:
                feature = featureExtactor.getFeature(frame)
                frameFeature.append(feature)
            features.append(frameFeature)
            labels.append(0 if motion == "we" else 1)

    return features,labels
if __name__ == "__main__":
    features,lables = getFeatureAndLabel()