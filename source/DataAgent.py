from feature_extractor import AttributeFilter, FeatureExtractor
from data_collection import Deserialization

import os
import numpy as np
import random
from feature_extractor import AttributeFilter


featureExtactor = FeatureExtractor()
def convertFramesToFeatures(frames):
    featureOfFrames = []
    for frame in frames:
        feature = featureExtactor.getFeature(frame)
        featureOfFrames.append(feature)
    return featureOfFrames


def getFeatureAndLabel():

    dynamicDataPath = os.path.abspath("../DynamicData")

    features = []
    labels = []
    duplicateIndexes =  AttributeFilter.getDuplicateIndexes()
    sampleDuplicator = SampleDuplicator(duplicateIndexes)

    for motion,label in [("we",0),("hello",1),("you",2),("teacher",3),("no",4),("eat",5)]:
        for i in range(1,501):
            leapFile = os.path.join(dynamicDataPath,"%s%s.lp"%(motion,i))
            if not os.path.exists(leapFile):
                continue
            de = Deserialization(leapFile)
            frames = de.frames
            featureOfFrames = []
            if len(frames) < 15:
                featureOfFrames = convertFramesToFeatures(frames)

                oscilatedSamples = sampleDuplicator.duplicate(featureOfFrames)

                features.extend(oscilatedSamples)
                labels.extend([label] * (len(featureOfFrames * sum(1 if CanDuplicate else 0 for CanDuplicate in duplicateIndexes))))

    indexes = [i for i in range(len(features))]

    random.shuffle(indexes)

    features_train = []
    features_test = []
    labels_train = []
    labels_test = []
    for i in range(int(len(features)*0.9)):
        features_train.append(features[indexes[i]])
        labels_train.append(labels[indexes[i]])

    for i in range(int(len(features) * 0.9),len(features)):
        features_test.append(features[indexes[i]])
        labels_test.append(labels[indexes[i]])

    return features_train,labels_train,features_test,labels_test

def getTrainingAndTestingData():
    features,labels = getFeatureAndLabel()


    for i in range(len(features)):
        t = random
class SampleDuplicator(object):
    """docstring for SampleDuplicator"""
    def __init__(self,targetIndexes):
         super(SampleDuplicator, self).__init__()
         self.targetIndexes = targetIndexes
    def duplicate(self,samples):
        duplicatedSamples = []
        
        for i in range(len(self.targetIndexes)):
            if self.targetIndexes[i] == True:
                for j in range(len(samples)):
                    copyOfSamples = self.copySamples(samples)
                    copyOfSamples[j][i] += 0.1 * np.random.rand()
                    duplicatedSamples.append(copyOfSamples)
        return duplicatedSamples


    
    def copySamples(self,samples):
        """
        samples should be a list of list, the inner list is feature of one frame, 
        the outer list contains features of frames belong to different timesteps
        """
        copy = [[val for val in sample] for sample in samples]
        return copy

if __name__ == "__main__":
    features_train,labels_train,features_test,labels_test = getFeatureAndLabel()
    print len(features_train)
    print len(labels_train)
    print len(features_test)
    print len(labels_test)
