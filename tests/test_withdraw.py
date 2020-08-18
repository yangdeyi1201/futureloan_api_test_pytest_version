# author:CC
# email:yangdeyi1201@foxmail.com

import pytest
from middleware.handler import Handler
from common.handler_request import visit_api
from common.handler_mysql import MysqlHandler
from decimal import Decimal

excel = Handler.excel
cases = excel.read_sheet('withdraw')


class TestWithdraw:
    @pytest.mark.parametrize('case_info', cases)
    @pytest.mark.parametrize('token', [Handler.yaml_conf['tester']], indirect=True)
    def test_withdraw(self, case_info, token, set_leaveamount_zero):
        url = Handler.yaml_conf['host']+case_info['url']
        method = case_info['method']

        headers = case_info['header'].replace('#testertoken#', token)
        headers = eval(headers)

        data = Handler().regular_replace(case_info['data'])
        data = eval(data)

        if '$' not in case_info['title'] and '*' not in case_info['title']:
            MysqlHandler().query('update member set leave_amount = {} where id = {};'.format(data['amount'], Handler.tester_id))

        if '*' in case_info['title']:
            MysqlHandler().query('update member set leave_amount = 0 where id = {};'.format(Handler.tester_id))

        if '&' not in case_info['title']:
            money_before = MysqlHandler().query('select leave_amount from member where id = {};'.format(Handler.tester_id))['leave_amount']
            withdraw_count_before = MysqlHandler().query('select count(*) from financelog where pay_member_id = {};'.format(Handler.tester_id))['count(*)']

        expected_resp = eval(case_info['expected_resp'])
        actual_resp = visit_api(url=url, method=method, headers=headers, json=data)

        try:
            for k, v in expected_resp.items():
                assert actual_resp[k] == v

            if '&' not in case_info['title']:
                money_after = MysqlHandler().query('select leave_amount from member where id = {};'.format(Handler.tester_id))['leave_amount']
                withdraw_count_after = MysqlHandler().query('select count(*) from financelog where pay_member_id = {};'.format(Handler.tester_id))['count(*)']

            if actual_resp['code'] == 0:
                assert money_before-Decimal(str(data['amount'])) == money_after
                assert withdraw_count_before + 1 == withdraw_count_after
            else:
                if '&' not in case_info['title']:
                    assert money_before == money_after
                    assert withdraw_count_after == withdraw_count_before
            Handler.success_case('withdraw', len(case_info), case_info['case_id'], __name__)

        except (AssertionError, TypeError):
            Handler.fail_case('withdraw', len(case_info), case_info['case_id'], __name__)
            raise

        finally:
            if '$' not in case_info['title']:
                MysqlHandler().query('update member set leave_amount = 0 where id = {};'.format(Handler.tester_id))


if __name__ == '__main__':
    pytest.main()
