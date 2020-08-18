# author:CC
# email:yangdeyi1201@foxmail.com

import pytest
from middleware.handler import Handler
from common.handler_request import visit_api
from common.handler_mysql import MysqlHandler

excel = Handler.excel
cases = excel.read_sheet('audit')


class TestAudit:
    @pytest.mark.parametrize('case_info', cases)
    @pytest.mark.parametrize('token', [Handler.yaml_conf['administrator']], indirect=True)
    @pytest.mark.parametrize('add_for_audit', [Handler.yaml_conf['tester']], indirect=True)
    def test_audit(self, case_info, token, add_for_audit):
        url = Handler.yaml_conf['host']+case_info['url']
        method = 'patch'

        headers = case_info['header'].replace('#admintoken#', token)
        headers = headers.replace('#testertoken#', add_for_audit)
        headers = eval(headers)

        data = Handler().regular_replace(case_info['data'])
        data = eval(data)

        sql = 'select `status` from loan where id = {};'.format(data['loan_id'])

        if '*' not in case_info['title']:
            bid_info_before = MysqlHandler().query(sql)

        expected_resp = eval(case_info['expected_resp'])
        actual_resp = visit_api(url=url, method=method, headers=headers, json=data)

        try:
            for k, v in expected_resp.items():
                assert actual_resp[k] == v

            if actual_resp['code'] == 0:
                bid_info = MysqlHandler().query(sql)
                if data['approved_or_not'] is True:
                    assert bid_info['status'] == 2
                elif data['approved_or_not'] is False:
                    assert bid_info['status'] == 5
            else:
                if '*' not in case_info['title']:
                    bid_info_after = MysqlHandler().query(sql)
                    assert bid_info_after['status'] == bid_info_before['status']
            Handler.success_case('audit', len(case_info), case_info['case_id'], __name__)
        except (AssertionError, TypeError):
            Handler.fail_case('audit', len(case_info), case_info['case_id'], __name__)
            raise


if __name__ == '__main__':
    pytest.main()
