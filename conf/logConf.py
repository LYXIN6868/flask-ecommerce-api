# 定义日志的基本操作
# 加载日志配置文件，得到打印日志的对象
import logging
import os
from logging import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 保证 logs 目录存在，避免日志文件写不进去
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

config.fileConfig(os.path.join(BASE_DIR, 'conf', 'log.conf'))
logger = logging.getLogger()

if __name__ == '__main__':
    logger.info('这是info日志')
    logger.error('这是错误日志')
    logger.debug('这是调试日志')
    logger.warning('这是警告日志')
