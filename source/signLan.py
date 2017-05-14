from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import tensorflow as tf
import numpy as np




HIDDEN_SIZE = 20
keep_prob = 0.5
BATCH_SIZE = 100
TIMESTEPS = 5
CLASS_NUM = 2

MAX_STEPS = 500
def inference(features):
	"""
	the forward function, it will caculate the final logits of the whole graph

	Args:
		features: [batch_size,dims],

	Returns:
		logits: [batch_size,64]
	"""
	with tf.variable_scope("rnn"):
		lstm_cell = tf.contrib.rnn.BasicLSTMCell(num_units=hidden_size, forget_bias=1.0, state_is_tuple=True)
		lstm_cell_dropout = tf.contrib.rnn.DropoutWrapper(cell=lstm_cell, input_keep_prob=1.0, output_keep_prob=keep_prob)
		#init_state = lstm_cell.zero_state(batch_size, dtype=tf.float32)
		outputs, state = tf.nn.dynamic_rnn(lstm_cell_dropout, inputs=X, dtype=tf.float32,time_major=False)
		h_state = outputs[:, -1, :] #[batch_size, hidden_size]

	with tf.variable_scope("fc"):

		weight = tf.get_variable("weight",[hidden_size,2],initializer=tf.truncated_normal_initializer(),dtype=tf.float32)
		bias = tf.get_variable("bias",[2],initializer=tf.constant_initializer())

		logits=tf.matmul(h_state,weight)+bias


	return logits

def loss(logits,labels):
	return tf.nn.sparse_softmax_cross_entropy_with_logits(logits,labels)

def optimize(loss):

	#TO DO: we need to add a decay learning rate
	optimizer = tf.train.AdamOptimizer(learning_rate=0.001)

	train_op = optimizer.minimize(loss)
	return train_op

def train():
	with tf.Graph().as_default():
		X = tf.placeholder(dtype=tf.float32,shape=[None,None,DIMS],name = "features")
		labels = tf.placeholder(dtype=tf.int32,shape=[None,1])

		logits = inference(X)
		train_loss = loss(logits,labels)
		train_op = optimize(train_loss)

		#saver = tf.train.Saver()
		with tf.Session() as sess:
			init = tf.global_variables_initializer()
			sess.run(init)

			for step in range(MAX_STEPS):
				loss,_ = sess.run([loss,train_op],feed_dict = {features:,labels:})

def Main():

