# author:CC
# email:yangdeyi1201@foxmail.com

import pytest
from middleware.handler import Handler
from common.handler_request import visit_api
from common.handler_mysql import MysqlHandler
import allure

excel = Handler.excel
cases = excel.read_sheet('register')


@allure.feature('注册接口')
class TestRegister:
    @pytest.mark.parametrize('case_info', cases)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_resister(self, case_info, member_before):
        url = Handler.yaml_conf['host'] + case_info['url']
        method = case_info['method']
        headers = eval(case_info['header'])

        data = Handler().regular_replace(case_info['data'])
        data = eval(data)

        expected_resp = eval(case_info['expected_resp'])
        actual_resp = visit_api(url=url, method=method, headers=headers, json=data)

        try:
            for k, v in expected_resp.items():
                assert actual_resp[k] == v

            member_after = MysqlHandler().query('select count(*) from member;')['count(*)']

            if actual_resp['code'] == 0:
                assert member_before + 1 == member_after
                amount_after = MysqlHandler().query('select leave_amount from member where mobile_phone = {}'.format(data['mobile_phone']))['leave_amount']
                assert amount_after == 0
            else:
                assert member_before == member_after
            Handler.success_case('register', len(case_info), case_info['case_id'], __name__)
        except (AssertionError, TypeError):
            Handler.fail_case('register', len(case_info), case_info['case_id'], __name__)
            raise


if __name__ == '__main__':
    pytest.main()
