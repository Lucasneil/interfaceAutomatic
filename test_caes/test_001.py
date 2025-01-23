import logging
from unittest import case

import pytest
import allure
from common.assert_api import AssertApi
from common.api_request import Api_Request
from common.read_exce_yaml_caes import get_yaml_excle_caes
import time

# 保留 get_cases 函数，但不需要在装饰器中直接调用
def get_cases():
    logging.debug("开始调用test001里的获取用例的逻辑了")
    print("开始调用test001里的获取用例的逻辑了")
    return get_yaml_excle_caes('test')

#@allure.epic(ReadFile.read_config("$.project_name"))  # 项目名称
class Test():
    # 移除原有的 @pytest.mark.parametrize 装饰器

    @allure.step
    def test_001(self, case, get_db, env_url):
        logging.debug(case)
        response = (Api_Request.api_data(case, env_url))
        assert AssertApi().assert_api(response, case, get_db)

# 使用 pytest_generate_tests 钩子函数动态生成测试用例
def pytest_generate_tests(metafunc):
    if "case" in metafunc.fixturenames:
        metafunc.parametrize("case", get_cases())