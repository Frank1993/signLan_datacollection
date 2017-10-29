from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import tensorflow as tf
import numpy as np

from DataAgent import getFeatureAndLabel


HIDDEN_SIZE = 100
KEEP_PROB = 0.7
BATCH_SIZE = 100
CLASS_NUM = 2

MAX_STEPS = 5000

DIMS = 26

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


	weight = tf.get_variable("weight",[HIDDEN_SIZE,6],initializer=tf.truncated_normal_initializer(),dtype=tf.float32)
	bias = tf.get_variable("bias",[6],initializer=tf.constant_initializer())

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


		weight = tf.get_variable("weight",[HIDDEN_SIZE,6],initializer=tf.truncated_normal_initializer(),dtype=tf.float32)
		bias = tf.get_variable("bias",[6],initializer=tf.constant_initializer())

		logits=tf.matmul(h_state,weight)+bias
		
		train_loss = GetLoss(logits,y)
		mean_loss = tf.reduce_mean(train_loss)

		correct_prediction = tf.argmax(logits, 1)
        #accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

		#tf.summary.scalar("losses",mean_loss)
		#tf.summary.scalar("accuracy",accuracy)

		train_op = optimize(train_loss)
		#summary_merged = tf.summary.merge_all()
		accs = []
		saver = tf.train.Saver()
		with tf.Session() as sess:
			init = tf.global_variables_initializer()
			sess.run(init)
			features_train,labels_train,features_test,labels_test = getFeatureAndLabel()
			#train_writer = tf.summary.FileWriter("./GraphAndSummary",sess.graph)
			for step in range(343677):
				#i = np.random.randint(0,len(features_train))
				i = step
				#print("***"*4 + "batch:" +"***"*4)
				#print(i)
				input_train = np.array(features_train[i])
				input_train = input_train[np.newaxis,:]

				label_train = np.array([labels_train[i]])
				#label = label[np.newaxis,:]
				#print(label)
				_ = sess.run([train_op],feed_dict = {X:input_train,y:label_train})
				#train_writer.add_summary(summary,step)
				#print(hstate)
				#print (lgts)
				#print(loss)

				if step % 1000 == 0:
					num_correct_predict = 0
					for j in range(len(features_test)):
						input_test = np.array(features_test[j])
						input_test = input_test[np.newaxis,:]
						label_test = np.array([labels_test[j]])

						predict_class = sess.run([correct_prediction],feed_dict = {X:input_test,y:label_test})
						if predict_class == label_test[0]:
							num_correct_predict += 1

					acc =  float(num_correct_predict)/len(features_test)
					print(acc)
					accs.append(acc)
					saver.save(sess,"./model2/SignClassifier",global_step = step)
		with open("./accracy") as f:
			for item in accs:
				f.write("%s\n"%item)

		#train_writer.close()

def Main():
	train()

if __name__ == "__main__":
	Main()
