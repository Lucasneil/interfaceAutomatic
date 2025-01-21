import logging,time, os
from loguru import logger as Logger
from common.all_path import logPath

# 日志文件路径
LOG_PATH = logPath
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

class PropogateHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)


logname = os.path.join(LOG_PATH, "{}.log".format(time.strftime("%Y%m%d")))
Logger.add(logname)
Logger.add(PropogateHandler(), format="{time:YYYY-MM-DD HH:mm:ss}|{message}", enqueue=True,)#enqueue=True, serialize=True

