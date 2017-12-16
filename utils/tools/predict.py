#! -*- utf-8 -*-

import os
import sys
import getopt
import yaml
import json
# import multiprocessing

from lib.predict import predict
from utils.tools.call_help import predictHelp
import config as conf


def predictAll():
    sess_mode_dir = os.path.join(os.getcwd(), conf.MODEL_SAVE_PATH)
    predict_models = os.listdir(sess_mode_dir)
    predictModels(predict_models)


def predictList(sess_models):
    sess_models = sess_models.split(",")
    predictModels(sess_models)


def predictModels(sess_mode_list):
    sess_mode_dir = os.path.join(os.getcwd(), conf.MODEL_SAVE_PATH)
    predict_result = {}
    for p_name in sess_mode_list:
        p_name = p_name.strip()
        sess_dir = os.path.join(sess_mode_dir, p_name)
        if not os.path.isdir(sess_dir):
            print('session "%s" model is not exist' % p_name)
            continue

        train_info_p = os.path.join(sess_dir, "train.info")
        if os.path.isfile(train_info_p):
            with open(train_info_p) as f:
                train_info = yaml.safe_load(f)
            print("train accuracy: %s" % train_info["accuracy"])
            # predictOne(train_info["conf_file"], p_name)

            try:
                pid = os.fork()
                if pid == 0:
                    result = predict(train_info["conf_file"], p_name)
                    result_save_path = os.path.join(os.getcwd(),
                                                    conf.RESULT_SAVE_PATH, p_name)

                    with open(result_save_path, 'w') as result_save_h:
                        result_save_h.write(json.dumps(result))

                    sys.exit(0)
                else:
                    os.waitpid(pid, 0)
                    # get from pipe[1]
            except Exception as ex:
                raise ex
        else:
            print("Predict Must define train.info")

    print(predict_result)


def run(argv):
    try:
        opts, args = getopt.getopt(argv, "hc:")
    except getopt.GetoptError:
        predictHelp(2)

    model_name = None
    for opt, arg in opts:
        if opt == '-h':
            predictHelp()
        if opt == "-c":
            model_name = arg

    if model_name is None:
        predictHelp()

    if model_name == "all":
        predictAll()
    else:
        predictList(model_name)
