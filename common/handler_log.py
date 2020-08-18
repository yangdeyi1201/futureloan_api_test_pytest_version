# author:CC
# email:yangdeyi1201@foxmail.com

import logging


def my_logger(file_path,
              logger_level='DEBUG', console_level='WARNING', file_level='INFO',
              fmt='<%(asctime)s>--<%(filename)s>--line:%(lineno)d--<%(levelname)s>--%(message)s'):

    logger = logging.getLogger()
    logger.setLevel(logger_level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(filename=file_path, mode='a', encoding='UTF-8')
    file_handler.setLevel(file_level)
    logger.addHandler(file_handler)

    console_handler.setFormatter(fmt=logging.Formatter(fmt=fmt))
    file_handler.setFormatter(fmt=logging.Formatter(fmt=fmt))

    return logger


if __name__ == '__main__':
    pass
