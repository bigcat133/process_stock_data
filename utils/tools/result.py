# -*- coding: utf-8 -*-

import os
# import sys
import getopt
import yaml
import json

import config as conf
from utils.tools.call_help import resultHelp


def checkTrainInfo(train_info, accuracy):
    accuracy = float(accuracy)
    info_list = []
    if train_info is None:
        sesses_path = os.path.join(os.getcwd(), conf.MODEL_SAVE_PATH)
        for _dir in os.listdir(sesses_path):
            model_path = os.path.join(sesses_path, _dir)
            if not os.path.isdir(model_path):
                continue
            with open(os.path.join(model_path, 'train.info'), 'r') as _info_fd:
                _info = yaml.safe_load(_info_fd.read())
                if _info['accuracy'] > accuracy:
                    info_list.append(_dir)
    return info_list


def getQualityStock(model_name, possibility):
    possibility = float(possibility)
    result_path = os.path.join(os.getcwd(), conf.RESULT_SAVE_PATH)
    model_res_path = os.path.join(result_path, model_name)
    if not os.path.isfile(model_res_path):
        return {}

    resultList = {}
    with open(model_res_path, 'r') as _result_fd:
        _result = json.loads(_result_fd.read())

        for stock_id in _result:
            if _result[stock_id][0] > possibility:
                resultList[stock_id] = _result[stock_id]
    return resultList


def run(argv):
    try:
        opts, args = getopt.getopt(argv, "hc:a:p:s:")
    except getopt.GetoptError as e:
        print(e)
        resultHelp(2)

    accuracy = 0.3
    possibility = 60
    train_info = None
    save_name = None
    for opt, arg in opts:
        if opt == '-h':
            resultHelp()
        elif opt == '-c':
            train_info = arg
        elif opt == '-a':
            accuracy = arg
        elif opt == "-p":
            possibility = arg
        elif opt == "-s":
            save_name = arg
    # print(accuracy, possibility, train_info)

    model_list = checkTrainInfo(train_info, accuracy)
    # print(model_list, len(model_list))
    all_quality = {}
    for model_name in model_list:
        quality = getQualityStock(model_name, possibility)
        for stack_id in quality:
            all_quality[stack_id] = quality[stack_id]

    if save_name is not None:
        save_path = os.path.join(os.getcwd(), save_name)
        with open(save_path, 'w') as save_fd:
            # save_fd.write(json.dumps(all_quality))
            for stock_id in all_quality:
                accur = all_quality[stock_id][0]
                _info = json.dumps(all_quality[stock_id][1])
                save_fd.write("%s: %s, %s\n" % (stock_id, accur, _info))

    print(len(all_quality))
