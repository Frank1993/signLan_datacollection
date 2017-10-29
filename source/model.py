from data_collection import Deserialization
from feature_extractor import FeatureExtractor

import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn import svm
import pickle
def train(model_path):
    records = []
    
    model_dir = '../StaticData/'
    for cla,file in [(0,"frameOf1.frame"),(1,"frameOf2.frame"),(2,"frameOf3.frame"),(3,"frameOf4.frame"),(4,"frameOf5.frame"),(5,"frameOf6.frame"),(6,"frameOf7.frame"),(7,"frameOf8.frame"),(8,"frameof9.frame")]:
        de = Deserialization(model_dir + file)
        frames = de.frames[100:-100]
    
        featureExtractor = FeatureExtractor()
        for frame in frames:
            frame_record = featureExtractor.getFeature(frame,cla)
            #print len(frame_record)
            records.append(frame_record)
    
    data = np.array(records)
    #print data.shape
    features = data[:,:-1]
    labels = data[:,-1]

    labels = labels.astype(int)
    print(np.unique(labels))
    print features.shape
    print labels.shape
    print type(labels[0])
    X_train, X_test, y_train, y_test = train_test_split(features,labels, test_size=0.2, random_state=42)


    clf = svm.SVC()
    y_train = y_train.astype(int)
    print(np.unique(y_train))
    clf.fit(X_train,y_train)
    
    predicted_test  = clf.predict(X_test)
    
    
    print np.mean(predicted_test == y_test)

    pickleFile = open(model_path,"w")
    pickle.dump(clf,pickleFile)
    pickleFile.close

def getClf(model_path = None):
    if model_path == None:
        model_path = "./staticModel/staticSVM.pkl"
    pickfile = open(model_path,"r")
    clf = pickle.load(pickfile)
    pickfile.close()
    return clf


if __name__ == "__main__":
    clf = train("./staticModel/staticSVM.pkl")

