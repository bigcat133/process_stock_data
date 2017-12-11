# -*- coding: utf-8 -*-

""" Neural Network.
run a rnn neural to process stock data
"""

from __future__ import print_function

import tensorflow as tf

from utils.tensorflow.session import save_sess
from utils.stock import Train
from config import (
    READ_TEST_DAY,
    READ_TEST_WIDTH,
    TEST_RESULT_WIDTH,
)


# Parameters
learning_rate = 0.1
num_steps = 500
batch_size = 128
display_step = 100

# Network Parameters
n_hidden_1 = 256  # 1st layer number of neurons
n_hidden_2 = 256  # 2nd layer number of neurons
num_input = READ_TEST_DAY * READ_TEST_WIDTH
num_classes = TEST_RESULT_WIDTH

# tf Graph input
X = tf.placeholder("float", [None, num_input])
Y = tf.placeholder("float", [None, num_classes])

# Store layers weight & bias
weights = {
    'h1': tf.Variable(tf.random_normal([num_input, n_hidden_1])),
    'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
    'out': tf.Variable(tf.random_normal([n_hidden_2, num_classes]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'b2': tf.Variable(tf.random_normal([n_hidden_2])),
    'out': tf.Variable(tf.random_normal([num_classes]))
}


# Create model
def neural_net(x):
    # Hidden fully connected layer with 256 neurons
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    # Hidden fully connected layer with 256 neurons
    layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'])
    # Output fully connected layer with a neuron for each class
    out_layer = tf.matmul(layer_2, weights['out']) + biases['out']
    return out_layer


def run(train_num=1, train_name=None, save_name=None):
    # Construct model
    logits = neural_net(X)
    prediction = tf.nn.softmax(logits)

    # Define loss and optimizer
    loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
        logits=logits, labels=Y))
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
    train_op = optimizer.minimize(loss_op)

    # Evaluate model
    correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    # Initialize the variables (i.e. assign their default value)
    init = tf.global_variables_initializer()

    # Start training
    with tf.Session() as sess:

        # Run the initializer
        sess.run(init)
        train = Train(train_name)
        batch_generator = train.next_batch(100)

        step = 0
        for batch in batch_generator:
            step += 1
            # batch_x, batch_y = mnist.train.next_batch(batch_size)
            # Run optimization op (backprop)
            sess.run(train_op, feed_dict={X: batch[0], Y: batch[1]})
            if step % display_step == 0 or step == 1:
                # Calculate batch loss and accuracy
                loss, acc = sess.run([loss_op, accuracy], feed_dict={X: batch[0],
                                                                     Y: batch[1]})
                print("Step {}, Minibatch Loss= {:.3f}, Training Accuracy= {:.2f}".format(
                    step, loss, acc))

        # Calculate accuracy for MNIST test images
        test_batch = train.test_batch()
        accur = sess.run(accuracy, feed_dict={X: test_batch[0],
                                              Y: test_batch[1]})
        # print("Multi Testing Accuracy: %s" % accur)
        if save_name:
            save_sess(sess, save_name)
        return accur
