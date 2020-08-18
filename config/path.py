# author:CC
# email:yangdeyi1201@foxmail.com

from pathlib import Path

# 当前文件绝对路径
current_path = Path(__file__).resolve()

# 项目根目录路径
root_path = current_path.parents[1]
# 测试数据目录路径
data_path = root_path/'data'
# 配置目录路径
config_path = root_path/'config'
# 日志目录路径
log_path = root_path/'logs'
# 报告目录路径
report_path = root_path/'reports'

if __name__ == '__main__':
    pass
