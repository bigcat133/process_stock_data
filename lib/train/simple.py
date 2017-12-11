# -*- coding: utf-8 -*-

import tensorflow as tf

from utils.tensorflow.session import save_sess
from utils.stock import Train
from config import (
    READ_TEST_DAY,
    READ_TEST_WIDTH,
    TEST_RESULT_WIDTH,
)


def run(train_num=1, train_name=None, save_name=None):
    sess = tf.InteractiveSession()
    x = tf.placeholder(tf.float32, shape=[
                       None, READ_TEST_DAY * READ_TEST_WIDTH])
    y_ = tf.placeholder(tf.float32, shape=[None, TEST_RESULT_WIDTH])

    W = tf.Variable(
        tf.zeros([READ_TEST_DAY * READ_TEST_WIDTH, TEST_RESULT_WIDTH]))
    b = tf.Variable(tf.zeros([TEST_RESULT_WIDTH]))

    sess.run(tf.global_variables_initializer())
    y = tf.matmul(x, W) + b
    cross_entropy = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits(logits=y, labels=y_))
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    i = 0
    for step in range(train_num):
        train = Train(train_name)
        batch_generator = train.next_batch(100)
        for batch in batch_generator:
            i += 1
            if i % 100 == 0:
                train_accuracy = accuracy.eval(
                    feed_dict={x: batch[0], y_: batch[1]})
                print("step %d, training accuracy %g" % (i, train_accuracy))
            train_step.run(feed_dict={x: batch[0], y_: batch[1]})

    # correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    # accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    test_batch = train.test_batch()
    test_batch = test_batch.__next__()
    accur = accuracy.eval(feed_dict={x: test_batch[0], y_: test_batch[1]})
    # print("simple test accuracy %g" % accur)

    if save_name:
        save_sess(sess, save_name)

    return accur
