# author:CC
# email:yangdeyi1201@foxmail.com

import pytest
from pathlib import Path
from config.path import report_path
import shutil

if __name__ == '__main__':
    allure_raw_path = report_path/'allure-raw'

    if Path.exists(allure_raw_path):
        shutil.rmtree(allure_raw_path)

    pytest.main(['alluredir=reports/allure-raw', '-s'])
