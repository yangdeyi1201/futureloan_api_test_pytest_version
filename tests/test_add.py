# author:CC
# email:yangdeyi1201@foxmail.com

import pytest
from middleware.handler import Handler
from common.handler_request import visit_api
from common.handler_mysql import MysqlHandler

excel = Handler.excel
cases = excel.read_sheet('add')


class TestAdd:
    @pytest.mark.parametrize('case_info', cases)
    @pytest.mark.parametrize('token', [Handler.yaml_conf['tester']], indirect=True)
    def test_add(self, case_info, token, admin_login, add_count_before_admin):
        url = Handler.yaml_conf['host']+case_info['url']
        method = 'post'

        headers = case_info['header'].replace('#testertoken#', token)
        headers = headers.replace('#admintoken#', admin_login)
        headers = eval(headers)

        data = Handler().regular_replace(case_info['data'])
        data = eval(data)

        if '*' not in case_info['title']:
            add_count_before_tester = MysqlHandler().query('select count(*) from loan where member_id = {};'.format(Handler.tester_id))['count(*)']

        expected_resp = eval(case_info['expected_resp'])
        actual_resp = visit_api(url, method, headers=headers, json=data)

        try:
            for k, v in expected_resp.items():
                assert actual_resp[k] == v

            if '&' in case_info['title']:
                add_count_after_admin = MysqlHandler().query('select count(*) from loan where member_id = {};'.format(Handler.administrator_id))['count(*)']
            else:
                if '*' not in case_info['title']:
                    add_count_after_tester = MysqlHandler().query('select count(*) from loan where member_id = {};'.format(Handler.tester_id))['count(*)']

            if actual_resp['code'] == 0:
                if '&' in case_info['title']:
                    add_count_before_admin+1 == add_count_after_admin
                else:
                    assert add_count_before_tester+1 == add_count_after_tester
            else:
                if '*' not in case_info['title']:
                    assert add_count_before_tester == add_count_after_tester
            Handler.success_case('add', len(case_info), case_info['case_id'], __name__)
        except (AssertionError, TypeError):
            Handler.fail_case('add', len(case_info), case_info['case_id'], __name__)
            raise


if __name__ == '__main__':
    pytest.main()
