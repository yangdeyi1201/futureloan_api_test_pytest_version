# author:CC
# email:yangdeyi1201@foxmail.com

import pytest
from middleware.handler import Handler
from common.handler_request import visit_api
from jsonpath import jsonpath
import allure

excel = Handler.excel
cases = excel.read_sheet('login')


@allure.feature('登录接口')
class TestLogin:
    @pytest.mark.parametrize('case_info', cases)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login(self, case_info):
        url = Handler.yaml_conf['host']+case_info['url']
        method = case_info['method']
        headers = eval(case_info['header'])
        data = eval(case_info['data'])

        actual_resp = visit_api(url=url, method=method, headers=headers, json=data)
        expected_resp = eval(case_info['expected_resp'])

        try:
            for k, v in expected_resp.items():
                assert actual_resp[k] == v

            if actual_resp['code'] == 0:
                assert jsonpath(actual_resp, '$..token')[0]
                assert jsonpath(actual_resp, '$..token_type')[0] == 'Bearer'
            Handler.success_case('login', len(case_info), case_info['case_id'], __name__)
        except (AssertionError, TypeError):
            Handler.fail_case('login', len(case_info), case_info['case_id'], __name__)
            raise


if __name__ == '__main__':
    pytest.main()
