# -*- coding:utf-8 -*-

import logging.config

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("example01")

logger.debug('This is debug message')
logger.info('This is info message')
logger.warning('This is warning message')


# 打印结果
result = " m = 无效提货"
if result.strip().find("无效提货编码") > -1:
    logger.info("{0} {1} = {2}".format(1, 2, result))
else:
    logger.warning("code {0} = {1}".format(1, result))
