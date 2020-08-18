# author:CC
# email:yangdeyi1201@foxmail.com

import requests


def visit_api(url, method, headers=None, json=None, data=None, params=None):
    return requests.request(url=url, method=method, headers=headers, json=json, data=data,params=params).json()


if __name__ == '__main__':
    pass
