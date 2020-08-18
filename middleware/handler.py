# author:CC
# email:yangdeyi1201@foxmail.com

from common.handler_excel import ExcelHandler
from common.handler_yaml import read_yaml
from common.handler_log import my_logger
from config.path import data_path, config_path, log_path
from common.handler_mysql import MysqlHandler


class Handler(object):
    excel = ExcelHandler(excel_path=data_path/'futureloan_api_test.xlsx')

    yaml_conf = read_yaml(yaml_path=config_path/'config.yaml')

    logger = my_logger(file_path=log_path/'log.log')

    investor_id = yaml_conf['investor_id']
    tester_id = yaml_conf['tester_id']
    administrator_id = yaml_conf['administrator_id']

    @property
    def randomphone(self):
        """随机生成手机号用于正常注册"""
        from random import randint
        return '138'+str(randint(10000000, 99999999))

    def regular_replace(self, string, pattern=r'#(.*?)#'):
        """正则替换"""
        import re
        while re.search(pattern=pattern, string=string):
            key = re.search(pattern=pattern, string=string).group(1)
            value = getattr(self, key, '')
            string = re.sub(pattern=pattern, repl=str(value), string=string, count=1)
        return string

    @property
    def not_exist_member_id(self):
        """取不存在的用户id"""
        max_member_id = MysqlHandler().query('select max(id) from member;')['max(id)']
        return max_member_id+1

    @property
    def other_member_id_more_than_zero(self):
        """取余额大于 0 元的非测试帐户 id"""
        id_more_than_zero = MysqlHandler().query('select id from member where leave_amount > 0 and id != 1026;')['id']
        return id_more_than_zero

    @property
    def loan_id_status_1(self):
        """取(借款)测试帐户最新借款的标id"""
        return MysqlHandler().query('select id from loan where member_id = 1026 and `status` = 1 order by create_time desc;')['id']

    @property
    def not_exist_loan_id(self):
        """取不存在的标id"""
        max_loan_id = MysqlHandler().query('select max(id) from loan;')['max(id)']
        return max_loan_id+1

    @property
    def loan_id_status_2(self):
        """取(借款)测试帐户竞标中状态的标id"""
        loan_id_status_1 = self.loan_id_status_1
        MysqlHandler().query('update loan set `status` = 2 where id = {}'.format(loan_id_status_1))
        return MysqlHandler().query('select id from loan where member_id = 1026 and `status` = 2 order by create_time desc;')['id']

    @property
    def loan_id_status_3(self):
        """取(借款)测试帐户还款中状态的标id"""
        loan_id_status_1 = self.loan_id_status_1
        MysqlHandler().query('update loan set `status` = 3 where id = {}'.format(loan_id_status_1))
        return MysqlHandler().query('select id from loan where member_id = 1026 and `status` = 3 order by create_time desc;')['id']

    @property
    def loan_id_status_4(self):
        """取(借款)测试帐户还款完成状态的标id"""
        loan_id_status_1 = self.loan_id_status_1
        MysqlHandler().query('update loan set `status` = 4 where id = {}'.format(loan_id_status_1))
        return MysqlHandler().query('select id from loan where member_id = 1026 and `status` = 4 order by create_time desc;')['id']

    @property
    def loan_id_status_5(self):
        """取(借款)测试帐户审核不通过状态的标id"""
        loan_id_status_1 = self.loan_id_status_1
        MysqlHandler().query('update loan set `status` = 5 where id = {}'.format(loan_id_status_1))
        return MysqlHandler().query('select id from loan where member_id = 1026 and `status` = 5 order by create_time desc;')['id']

    @staticmethod
    def success_case(sheet_name, column, case_id, module_name):
        """用例通过：excel回写测试结果+输出日志"""
        Handler.excel.write(sheet_name=sheet_name, row=case_id+1, column=column, data='pass')
        Handler.logger.info('{}--第{}条测试用例通过'.format(module_name, case_id))

    @staticmethod
    def fail_case(sheet_name, column, case_id, module_name):
        """用例失败：excel回写测试结果+输出日志"""
        Handler.excel.write(sheet_name=sheet_name, row=case_id+1, column=column, data='fail')
        Handler.logger.error('{}--第{}条测试用例不通过'.format(module_name, case_id))


if __name__ == '__main__':
    pass
