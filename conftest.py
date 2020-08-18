# author:CC
# email:yangdeyi1201@foxmail.com

import pytest
from common.handler_mysql import MysqlHandler
from common.handler_request import visit_api
from middleware.handler import Handler
from jsonpath import jsonpath


@pytest.fixture(scope='function')
def member_before():
    """注册前查询 member 表记录条数"""
    member_count_before = MysqlHandler().query(sql='select count(*) from member;')['count(*)']
    yield member_count_before


@pytest.fixture(scope='class')
def token(request):
    """
    不同账户登录
    返回 不同帐户登录 token
    """
    user = request.param
    url = Handler.yaml_conf['host']+'/member/login'
    method = 'post'
    headers = {'X-Lemonban-Media-Type': 'lemonban.v2'}
    data = user
    resp = visit_api(url=url, method=method, headers=headers, json=data)
    token_type = jsonpath(resp, '$..token_type')[0]
    token_value = jsonpath(resp, '$..token')[0]
    yield token_type+' '+token_value


@pytest.fixture(scope='class')
def set_leaveamount_zero():
    """提现测试类执行前后置零测试帐户余额"""
    MysqlHandler().query('update member set leave_amount = 0 where id = 1026;')
    yield
    MysqlHandler().query('update member set leave_amount = 0 where id = 1026;')


@pytest.fixture(scope='class')
def add_count_before_admin():
    """加标测试类执行前获取管理员帐户借款标记录条数"""
    yield MysqlHandler().query('select count(*) from loan where member_id = {};'.format(Handler.administrator_id))['count(*)']


@pytest.fixture(scope='class')
def add_for_invest(request):
    """
    1、借款帐户登录取得 token
    2、投资测试类执行前先为借款帐户加一个标并审核状态为竞标中
    3、返回 借款帐户登录 token 和新加标 id
    """
    tester = request.param

    resp_login = visit_api(url=Handler.yaml_conf['host']+'/member/login', method='post',
                           headers={'X-Lemonban-Media-Type': 'lemonban.v2'}, json=tester)
    tester_token = jsonpath(resp_login, '$..token_type')[0]+' '+jsonpath(resp_login, '$..token')[0]

    add_headers = {'X-Lemonban-Media-Type': 'lemonban.v2', 'Authorization': tester_token}
    bid_data = {'member_id': Handler.tester_id, 'title': 'CC拿offer', 'amount': 50000,
                'loan_rate': 12.0, 'loan_term': 3, 'loan_date_type': 1, 'bidding_days': 3}

    resp_add = visit_api(Handler.yaml_conf['host']+'/loan/add', 'post', headers=add_headers, json=bid_data)
    new_loan_id = jsonpath(resp_add, '$..id')[0]
    MysqlHandler().query('update loan set `status` = 2 where id = {};'.format(new_loan_id))
    yield tester_token, new_loan_id


@pytest.fixture(scope='function')
def add_for_audit(request):
    """
    1、借款帐户登录取得 token
    2、每条审核用例执行都先加标
    3、返回 借款帐户登录 token
    """
    tester = request.param

    resp_login = visit_api(url=Handler.yaml_conf['host']+'/member/login', method='post',
                           headers={'X-Lemonban-Media-Type': 'lemonban.v2'}, json=tester)
    tester_token = jsonpath(resp_login, '$..token_type')[0]+' '+jsonpath(resp_login, '$..token')[0]

    add_headers = {'X-Lemonban-Media-Type': 'lemonban.v2', 'Authorization': tester_token}
    bid_data = {'member_id': Handler.tester_id, 'title': 'CC测审核', 'amount': 50000,
                'loan_rate': 12.0, 'loan_term': 3, 'loan_date_type': 1, 'bidding_days': 3}

    visit_api(Handler.yaml_conf['host']+'/loan/add', 'post', headers=add_headers, json=bid_data)
    yield tester_token


@pytest.fixture(scope='class')
def admin_login():
    """
    管理员测试帐户登录
    返回 管理员登录 token
    """
    resp_login = visit_api(url=Handler.yaml_conf['host']+'/member/login', method='post',
                           headers={'X-Lemonban-Media-Type': 'lemonban.v2'}, json=Handler.yaml_conf['administrator'])
    admin_token = jsonpath(resp_login, '$..token_type')[0]+' '+jsonpath(resp_login, '$..token')[0]
    yield admin_token


@pytest.fixture(scope='class')
def recharge_before_invest_and_set_zero_after():
    """
    投资测试类执行前预充值所有测试帐户
    投资测试类执行后置零所有测试帐户余额
    """
    MysqlHandler().query('update member set leave_amount = 150000 where id = {};'.format(Handler.investor_id))
    MysqlHandler().query('update member set leave_amount = 1000 where id in ({}, {});'.format(Handler.tester_id, Handler.administrator_id))
    yield
    MysqlHandler().query('update member set leave_amount = 0 where id in ({}, {}, {});'.format(Handler.investor_id, Handler.tester_id, Handler.administrator_id))
