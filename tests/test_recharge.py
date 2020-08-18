# author:CC
# email:yangdeyi1201@foxmail.com

import pytest
from middleware.handler import Handler
from common.handler_request import visit_api
from common.handler_mysql import MysqlHandler
from decimal import Decimal
import allure

excel = Handler.excel
cases = excel.read_sheet('recharge')


@allure.feature('充值接口')
class TestRecharge:
    @pytest.mark.parametrize('case_info', cases)
    @pytest.mark.parametrize('token', [Handler.yaml_conf['tester']], indirect=True)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_recharge(self, case_info, token):
        url = Handler.yaml_conf['host']+case_info['url']
        method = case_info['method']

        headers = case_info['header'].replace('#testertoken#', token)
        headers = eval(headers)

        data = Handler().regular_replace(case_info['data'])
        data = eval(data)

        if '*' not in case_info['title']:
            money_before = MysqlHandler().query('select leave_amount from member where id = {};'.format(Handler.tester_id))['leave_amount']
            recharge_count_before = MysqlHandler().query(sql='select count(*) from financelog where income_member_id = {};'.format(Handler.tester_id))['count(*)']

        expected_resp = eval(case_info['expected_resp'])
        actual_resp = visit_api(url=url, method=method, headers=headers, json=data)

        try:
            for k, v in expected_resp.items():
                assert actual_resp[k] == v

            if '*' not in case_info['title']:
                money_after = MysqlHandler().query('select leave_amount from member where id = {};'.format(Handler.tester_id))['leave_amount']
                recharge_count_after = MysqlHandler().query('select count(*) from financelog where income_member_id = {};'.format(Handler.tester_id))['count(*)']

            if actual_resp['code'] == 0:
                assert money_before+Decimal(str(data['amount'])) == money_after
                assert recharge_count_before+1 == recharge_count_after
            else:
                if '*' not in case_info['title']:
                    assert money_before == money_after
                    assert recharge_count_before == recharge_count_after
            Handler.success_case('recharge', len(case_info), case_info['case_id'], __name__)
        except (AssertionError, TypeError):
            Handler.fail_case('recharge', len(case_info), case_info['case_id'], __name__)
            raise


if __name__ == '__main__':
    pytest.main()
