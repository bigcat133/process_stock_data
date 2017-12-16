# -*- coding: utf-8 -*-

""" Recurrent Neural Network.

A Recurrent Neural Network (LSTM) implementation example using TensorFlow library.
This example is using the MNIST database of handwritten digits (http://yann.lecun.com/exdb/mnist/)

Links:
    [Long Short Term Memory](http://deeplearning.cs.cmu.edu/pdfs/Hochreiter97_lstm.pdf)
    [MNIST Dataset](http://yann.lecun.com/exdb/mnist/).

Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
"""

from __future__ import print_function

import numpy as np
import tensorflow as tf
from tensorflow.contrib import rnn

from utils.tensorflow.session import save_sess
from utils.stock import Train
from config import (
    READ_TEST_DAY,
    READ_TEST_WIDTH,
    TEST_RESULT_WIDTH,
    READ_LOG_LONG,
)


'''
To classify images using a recurrent neural network, we consider every image
row as a sequence of pixels. Because MNIST image shape is 28*28px, we will then
handle 28 sequences of 28 steps for every sample.
'''

# Training Parameters
learning_rate = 0.001
training_steps = 10000
batch_size = READ_LOG_LONG
display_step = 200

# Network Parameters
num_input = READ_TEST_WIDTH
timesteps = READ_TEST_DAY  # timesteps
num_hidden = 128  # hidden layer num of features
num_classes = TEST_RESULT_WIDTH  # MNIST total classes (0-9 digits)

# tf Graph input
X = tf.placeholder("float", [None, timesteps, num_input], name="input_list")
Y = tf.placeholder("float", [None, num_classes])


def RNN(x):

    # Prepare data shape to match `rnn` function requirements
    # Current data input shape: (batch_size, timesteps, n_input)
    # Required shape: 'timesteps' tensors list of shape (batch_size, n_input)

    # Unstack to get a list of 'timesteps' tensors of shape (batch_size, n_input)
    x = tf.unstack(x, timesteps, 1)

    with tf.variable_scope('lstm1', reuse=tf.AUTO_REUSE):
        # Define a lstm cell with tensorflow
        lstm_cell = rnn.BasicLSTMCell(num_hidden, forget_bias=1.0)

        # Get lstm cell output
        outputs, states = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)

    # Define weights
    weights = tf.Variable(tf.random_normal([num_hidden, num_classes]))
    biases = tf.Variable(tf.random_normal([num_classes]))
    # Linear activation, using rnn inner loop last output
    return tf.add(tf.matmul(outputs[-1], weights), biases, name="result_list")


def train_run(sess, loss_op, train_op, accuracy, train_name=None, train_num=1):
    train = Train(train_name)
    for step in range(train_num):
        train.init()
        batch_generator = train.next_batch(batch_size)
        batch_x, batch_y = None, None
        for batch in batch_generator:
            batch_x, batch_y = batch
            batch_x = np.array(batch_x, np.float32)
            # Reshape data to get 28 seq of 28 elements
            batch_x = batch_x.reshape((batch_size, timesteps, num_input))
            batch_x = batch_x[:: -1]
            # Run optimization op (backprop)
            sess.run(train_op, feed_dict={X: batch_x, Y: batch_y})

        if batch_x is None or batch_y is None:
            print(train_name, "format error!!!!!!!!!!!")

        # Calculate batch loss and accuracy
        loss, acc = sess.run([loss_op, accuracy],
                             feed_dict={X: batch_x,
                                        Y: batch_y})
        print("Step {}, Minibatch Loss= {:.4f}, Training Accuracy= {:.3f}".format(
            step, loss, acc))

    result_prop = 0
    _t_step = 0
    for test, result in train.test_batch(batch_size):
        _b_size = len(test)
        test = np.array(test, np.float32)
        test = test.reshape((_b_size, timesteps, num_input))
        test = test[:: -1]
        accur = sess.run(accuracy, feed_dict={X: test,
                                              Y: result})
        result_prop += accur
        _t_step += 1
        if _t_step % 10 == 0:
            print("RNN step %s Testing Accuracy: %s" %
                  (_t_step, accur))

    # train.clean()

    accur = result_prop / _t_step
    return accur


def run(train_num=1, train_name=None, save_name=None):
    logits = RNN(X)
    prediction = tf.nn.softmax(logits, name="result_var")

    # Define loss and optimizer
    loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
        logits=logits, labels=Y))
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
    train_op = optimizer.minimize(loss_op)

    # Evaluate model (with test logits, for dropout to be disabled)
    correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32), name="accuracy")

    # Initialize the variables (i.e. assign their default value)
    init = tf.global_variables_initializer()

    # Start training
    with tf.Session() as sess:

        # Run the initializer
        sess.run(init)
        accur = train_run(sess, loss_op, train_op, accuracy, train_name, train_num)
        if save_name:
            save_sess(sess, save_name, accur, train_name)
        return accur
