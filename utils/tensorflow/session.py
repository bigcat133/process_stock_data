# -*- coding: utf-8 -*-

import os

import tensorflow as tf

from config import (
    MODEL_SAVE_PATH
)


def save_sess(sess, save_model, accuracy=None, conf=None):
    _save_dir = os.path.join(MODEL_SAVE_PATH, save_model)
    if not os.path.exists(_save_dir):
        os.makedirs(_save_dir)
    saver = tf.train.Saver()
    _save_path = os.path.join(_save_dir, save_model)
    saver.save(sess, _save_path)

    if accuracy is not None or conf is not None:
        info_path = os.path.join(_save_dir, "train.info")
        with open(info_path, 'w') as info_f:
            if accuracy is not None:
                info_f.write("accuracy: %s\n" % accuracy)
            if conf is not None:
                info_f.write("conf_file: %s\n" % conf)


def load_sess(sess, load_model):
    _base_path = os.path.join(MODEL_SAVE_PATH, load_model)
    _graph_n = "%s.meta" % load_model
    load_graph_path = os.path.join(_base_path, _graph_n)
    saver = tf.train.import_meta_graph(load_graph_path)
    saver.restore(sess, tf.train.latest_checkpoint(_base_path))

    return sess
