import logging
import os
import pytest
import allure
from common.assert_api import AssertApi
from common.api_request import Api_Request
from common.read_exce_yaml_caes import get_yaml_excle_caes
from common.exchange_data import ExchangeData

def get_cases():
    logging.debug("开始调用test001里的获取用例的逻辑了")
    print("开始调用test001里的获取用例的逻辑了")
    #task_id = ExchangeData.get_task_id()  # 获取当前线程的 task_id
    return get_yaml_excle_caes('test')

class Test:
    @allure.step
    def test_001(self, case, get_db, env_url):
        logging.debug(case)
        response = (Api_Request.api_data(case, env_url))
        assert AssertApi().assert_api(response, case, get_db)

def pytest_generate_tests(metafunc):
    logging.debug("开始调用test001的逻辑了")
    if "case" in metafunc.fixturenames:
        task_id = ExchangeData.get_task_id()  # 获取当前线程的 task_id
        logging.debug(f"Current Task ID1111: {task_id}")
        cases = get_cases()
        logging.debug(f"Generated cases: {cases}")
        metafunc.parametrize("case", cases)
    else:
        logging.debug("No 'case' in fixturenames")