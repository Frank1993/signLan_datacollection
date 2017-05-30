from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import tensorflow as tf
import numpy as np

from DataAgent import getFeatureAndLabel


HIDDEN_SIZE = 100
KEEP_PROB = 0.5
BATCH_SIZE = 100
TIMESTEPS = 5
CLASS_NUM = 2

MAX_STEPS = 5000

DIMS = 311

def inference(features):
	"""
	the forward function, it will caculate the final logits of the whole graph

	Args:
		features: [batch_size,dims],

	Returns:
		logits: [batch_size,64]
	"""
	lstm_cell = tf.contrib.rnn.BasicLSTMCell(num_units=HIDDEN_SIZE, forget_bias=1.0, state_is_tuple=True)
	lstm_cell_dropout = tf.contrib.rnn.DropoutWrapper(cell=lstm_cell, input_keep_prob=1.0, output_keep_prob=KEEP_PROB)
	#init_state = lstm_cell.zero_state(batch_size, dtype=tf.float32)
	outputs, state = tf.nn.dynamic_rnn(lstm_cell_dropout, inputs=features, dtype=tf.float32,time_major=False)
	h_state = outputs[:, -1, :] #[batch_size, hidden_size]


	weight = tf.get_variable("weight",[HIDDEN_SIZE,2],initializer=tf.truncated_normal_initializer(),dtype=tf.float32)
	bias = tf.get_variable("bias",[2],initializer=tf.constant_initializer())

	logits=tf.matmul(h_state,weight)+bias


	return logits

def GetLoss(logits,labels):

	return tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits,labels=labels)

def optimize(loss):

	#TO DO: we need to add a decay learning rate
	optimizer = tf.train.AdamOptimizer(learning_rate=0.001)

	train_op = optimizer.minimize(loss)
	return train_op

def train():
	with tf.Graph().as_default():
		X = tf.placeholder(dtype=tf.float32,shape=[None,None,DIMS],name = "features")
		y = tf.placeholder(dtype=tf.int32,shape=[None])

		lstm_cell = tf.contrib.rnn.BasicLSTMCell(num_units=HIDDEN_SIZE, forget_bias=0.4, state_is_tuple=True)
		lstm_cell_dropout = tf.contrib.rnn.DropoutWrapper(cell=lstm_cell, input_keep_prob=1.0, output_keep_prob=KEEP_PROB)
		#init_state = lstm_cell.zero_state(batch_size, dtype=tf.float32)
		outputs, state = tf.nn.dynamic_rnn(lstm_cell_dropout, inputs=X, dtype=tf.float32,time_major=False)
		h_state = outputs[:, -1, :] #[batch_size, hidden_size]


		weight = tf.get_variable("weight",[HIDDEN_SIZE,2],initializer=tf.truncated_normal_initializer(),dtype=tf.float32)
		bias = tf.get_variable("bias",[2],initializer=tf.constant_initializer())

		logits=tf.matmul(h_state,weight)+bias
		
		train_loss = GetLoss(logits,y)
		train_op = optimize(train_loss)

		#saver = tf.train.Saver()
		with tf.Session() as sess:
			init = tf.global_variables_initializer()
			sess.run(init)
			features,labels = getFeatureAndLabel()
			test_losses = []
			for step in range(MAX_STEPS):
				i = np.random.randint(0,len(features))
				#print("***"*4 + "batch:" +"***"*4)
				#print(i)
				feature = np.array(features[i])
				feature = feature[np.newaxis,:]

				label = np.array([labels[i]])
				#label = label[np.newaxis,:]
				#print(label)
				loss,_ = sess.run([train_loss,train_op],feed_dict = {X:feature,y:label})
				#print(hstate)
				#print (lgts)
				#print(loss)
				test_losses.append(loss)

			with open("/Users/hu/tmp/losses.txt",'w') as f:
				for l in test_losses:
					f.write("%s,\n"%l)

def Main():
	train()

if __name__ == "__main__":
	Main()
