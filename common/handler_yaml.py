# author:CC
# email:yangdeyi1201@foxmail.com

import yaml


def read_yaml(yaml_path):
    """读取yaml文件"""
    with open(file=yaml_path, mode='rb') as f:
        yaml_file = f.read()
    yaml_conf = yaml.full_load(stream=yaml_file)
    return yaml_conf


if __name__ == '__main__':
    pass
