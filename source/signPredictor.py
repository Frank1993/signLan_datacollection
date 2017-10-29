import tensorflow as tf

import os
from DataAgent import convertFramesToFeatures
import numpy as np

"""
dynamicDataPath = os.path.abspath("../DynamicData")
leapFile = os.path.join(dynamicDataPath,"%s%s.lp"%("hello",55))
from data_collection import Deserialization
de = Deserialization(leapFile)
frames = de.frames
features = convertFramesToFeatures(frames)
"""
sess = tf.Session()

checkpoint_state = tf.train.get_checkpoint_state("./model2")
checkpoint_path = checkpoint_state.model_checkpoint_path
saver = tf.train.import_meta_graph(checkpoint_path+".meta")
saver.restore(sess,checkpoint_path)

logits = sess.graph.get_tensor_by_name("add:0")
X = sess.graph.get_tensor_by_name("features:0")

def predict(features):
    input_test = np.array(features)
    input_test = input_test[np.newaxis,:]
    logits_ = sess.run([logits],feed_dict = {X:input_test})
    return np.argmax(logits_)
    



