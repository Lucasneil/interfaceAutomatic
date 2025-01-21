import pytest,allure
from common.assert_api import AssertApi
from common.api_request import Api_Request
from common.read_exce_yaml_caes import get_yaml_excle_caes
import time


#@allure.epic(ReadFile.read_config("$.project_name"))  # 项目名称
class Test():
    @pytest.mark.parametrize("case",get_yaml_excle_caes('test'))
    @allure.step
    def test_001(self,case,get_db,env_url):

        response = (Api_Request.api_data(case, env_url))
        assert AssertApi().assert_api(response, case, get_db)





