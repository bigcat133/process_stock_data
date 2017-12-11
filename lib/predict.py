#! -*- utf-8 -*-

import os
import sys
from decimal import Decimal

from utils.reader import (
    readLastData
)
import config as conf


def _calc_result(result_var):
    result = [float(Decimal(i*100).quantize(Decimal('0.00'))) for i in result_var]

    sum_v = float(Decimal(sum(result[0:3])).quantize(Decimal('0.00')))
    return sum_v, result


def _run(model_name, stock_code_list):
    import tensorflow as tf

    from utils.tensorflow.session import (
        load_sess,
    )

    _model_dir = os.path.join(os.getcwd(), conf.MODEL_SAVE_PATH)
    model_path = os.path.join(_model_dir, model_name)
    if not os.path.isdir(model_path):
        print("model %s do not exist" % model_name)
        return

    result_dict = {}

    with tf.Session() as sess:
        sess = load_sess(sess, model_name)
        graph = tf.get_default_graph()
        input_data = graph.get_tensor_by_name("input_list:0")
        for stock_code in stock_code_list:
            stock_name = "%s.log" % stock_code
            stock_path = os.path.join(conf.STOCK_DATA_PATH, stock_name)
            if not os.path.exists(stock_path):
                print("stock(%s) do not exist" % stock_name)
                continue
            feed_dict = {input_data: readLastData(stock_name)}
            result_var = graph.get_tensor_by_name("result_var:0")
            result_list = graph.get_tensor_by_name("result_list:0")
            print("##########result(%s)###########" % stock_code)
            try:
                _r_var, _r_list = sess.run([result_var, result_list], feed_dict)
                # print(_r_var[0], _r_list[0])
                rise_ratio, ratio_list = _calc_result(_r_var[0])
                result_dict[stock_code] = [rise_ratio, ratio_list]
                print(result_dict[stock_code])
            except Exception:
                pass
            print("###############################\n")
    # print(model_path, stock_code_list)
    return result_dict


def predict(stock_conf, model_name):

    _conf_dir = os.path.join(os.getcwd(), conf.TYPE_CONF_DIR)
    type_conf = os.path.join(_conf_dir, stock_conf)
    if not os.path.exists(type_conf):
        print("type conf %s do not exist" % type_conf)
        sys.exit(100)
    stock_code_list = []
    with open(type_conf, 'r') as train_conf_f:
        for stock_code in train_conf_f:
            stock_code_list.append(stock_code.strip())

    return _run(model_name, stock_code_list)
