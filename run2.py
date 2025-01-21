#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# @Time    : 2022/8/18 20:42
# @Author  : mojin
# @Email   : 397135766@qq.com
# @File    : run.py
# @Software: PyCharm
#-------------------------------------------------------------------------------


import pytest,shutil,subprocess
from shutil import copy
from common.read_file import ReadFile
from common import all_path
from common.exchange_data import ExchangeData




def run():


    try:
        shutil.rmtree(all_path.targetPath) #删除allure历史数据
    except:
        pass
    # --reruns = 3  失败重试
    pytest.main(['./test_caes', '-vs'])


    copy(all_path.Start_server_bat, all_path.targetPath)


    allure_html = 'allure generate ./target/allure-results -o ./target/allure-report --clean'  # 生成allure的html报告
    subprocess.call(allure_html, shell=True)  # 生成allure的html报告




if __name__ == '__main__':
    run()
