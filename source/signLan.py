from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import tensorflow as tf

BATCH_SIZE = 100
DIMS = 63

MAX_STEPS = 5000

def inference(features):
	"""
	the forward function, it will caculate the final logits of the whole graph

	Args:
		features: [batch_size,dims],

	Returns:
		logits: [batch_size,64]
	"""

	batch_size,dims = tf.shape(features)

	with tf.variable_scope("fc1"):
		weight = tf.get_variable("weight",[dims,128],initializer=tf.truncated_normal_initializer(),dtype=tf.float32)
		bias = tf.get_variable("bias",[128],initializer=tf.constant_initializer())

		fc1=tf.matmul(features,weight)+bias

		relu1 = tf.nn.relu(fc1)


	with tf.variable_scope("fc2"):
		weight = tf.get_variable("weight",[dims,64],initializer=tf.truncated_normal_initializer(),dtype=tf.float32)
		bias = tf.get_variable("bias",[64],initializer=tf.constant_initializer())

		logits=tf.matmul(relu1,weight)+bias

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
		features = tf.placeholder(dtype=tf.float32,shape=[BATCH_SIZE,DIMS],name = "features")
		labels = tf.placeholder(dtype=tf.int32,shape=[bat])

		loss = inference(features)

		train_op = optimize(loss)

		saver = tf.train.Saver()
		with tf.Session() as sess:

			for step in range(MAX_STEPS):
				loss,_ = sess.run([loss,train_op],feed_dict = {features:,labels:})

def Main():

