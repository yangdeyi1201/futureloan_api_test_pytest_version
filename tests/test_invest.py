# author:CC
# email:yangdeyi1201@foxmail.com

import pytest
from middleware.handler import Handler
from common.handler_request import visit_api
from common.handler_mysql import MysqlHandler

excel = Handler.excel
cases = excel.read_sheet('invest')


class TestInvest:
    @pytest.mark.parametrize('case_info', cases)
    @pytest.mark.parametrize('token', [Handler.yaml_conf['investor']], indirect=True)
    @pytest.mark.parametrize('add_for_invest', [Handler.yaml_conf['tester']], indirect=True)
    def test_invest(self, case_info, token, admin_login, recharge_before_invest_and_set_zero_after, add_for_invest):
        url = Handler.yaml_conf['host']+case_info['url']
        method = 'post'

        headers = case_info['header'].replace('#invest_token#', token)
        headers = headers.replace('#testertoken#', add_for_invest[0])
        headers = headers.replace('#admintoken#', admin_login)
        headers = eval(headers)

        if '#loan_id_status_2#' in case_info['data']:
            data = case_info['data'].replace('#loan_id_status_2#', str(add_for_invest[1]))
            data = Handler().regular_replace(data)
        else:
            data = Handler().regular_replace(case_info['data'])
        data = eval(data)

        if data['member_id'] in (Handler.investor_id, Handler.tester_id, Handler.administrator_id):
            invest_count_before_list = MysqlHandler().query('select count(*) from invest where member_id = {} or member_id = {} or member_id = {} group by member_id;'.format(Handler.tester_id, Handler.investor_id, Handler.administrator_id), one=False)

            if data['member_id'] == Handler.investor_id:
                investor_count_before = invest_count_before_list[2]['count(*)']
            elif data['member_id'] == Handler.tester_id:
                tester_count_before = invest_count_before_list[0]['count(*)']
            elif data['member_id'] == Handler.administrator_id:
                administrator_count_before = invest_count_before_list[1]['count(*)']

        expected_resp = eval(case_info['expected_resp'])
        actual_resp = visit_api(url=url, method=method, headers=headers, json=data)

        try:
            for k, v in expected_resp.items():
                assert actual_resp[k] == v

            if data['member_id'] in (Handler.investor_id, Handler.tester_id, Handler.administrator_id):
                invest_count_after_list = MysqlHandler().query('select count(*) from invest where member_id = {} or member_id = {} or member_id = {} group by member_id;'.format(Handler.tester_id, Handler.investor_id, Handler.administrator_id), one=False)

                if data['member_id'] == Handler.investor_id:
                    investor_count_after = invest_count_after_list[2]['count(*)']
                elif data['member_id'] == Handler.tester_id:
                    tester_count_after = invest_count_after_list[0]['count(*)']
                elif data['member_id'] == Handler.administrator_id:
                    administrator_count_after = invest_count_after_list[1]['count(*)']

            if actual_resp['code'] == 0:
                if data['member_id'] == Handler.investor_id:
                    assert investor_count_before+1 == investor_count_after
                elif data['member_id'] == Handler.tester_id:
                    assert tester_count_before+1 == tester_count_after
                elif data['member_id'] == Handler.administrator_id:
                    assert administrator_count_before+1 == administrator_count_after
            else:
                if data['member_id'] == Handler.investor_id:
                    assert investor_count_before == investor_count_after
            Handler.success_case('invest', len(case_info), case_info['case_id'], __name__)
        except (AssertionError, TypeError):
            Handler.fail_case('invest', len(case_info), case_info['case_id'], __name__)
            raise


if __name__ == '__main__':
    pytest.main()
