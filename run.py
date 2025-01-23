import logging

import pytest,shutil,subprocess
from shutil import copy
from common.read_file import ReadFile
from common import all_path
from common.exchange_data import ExchangeData
import time

def run():


    # --reruns = 3  失败重试
    pytest.main(['./test_caes', '-vs', "--env=test", "--alluredir", "./target/allure-results" ])  # pytest测试框架主程序运行
    #pytest.main(['./test_caes', '-vs', "--env=test"])  # pytest测试框架主程序运行
    logging.debug("开始调用run了")
    # copy(all_path.Start_server_bat, all_path.targetPath)
    #allure_html = 'allure generate ./target/allure-results -o ./target/allure-report --clean'  # 生成allure的html报告
    #subprocess.call(allure_html, shell=True)  # 生成allure的html报告




if __name__ == '__main__':
    run()
