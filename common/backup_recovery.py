import os
from common.logger import Logger


class BackupRecovery:
    def __init__(self, db_data,):
        self.host = db_data['host']
        self.user = db_data['user']
        self.password = db_data['password']
        self.database = db_data['database']
        self.port = db_data['port']

    def backup(self, db_path):
        backup_cmd=f'mysqldump --column-statistics=0 -h{self.host} -u{self.user} -p{self.password} -P{self.port} {self.database} > {db_path}'
        Logger.info(backup_cmd)
        code = os.system(backup_cmd)
        if code == 0:
            Logger.warning(f'备份[{db_path}]数据库执行成功！')
        else:
            Logger.error(f'备份[{db_path}]数据库执行失败！（{code}）')

    def recovery(self, db_path):
        backup_cmd=f'mysql -h{self.host} -u{self.user} -p{self.password} -P{self.port} {self.database} < {db_path}'
        Logger.info(backup_cmd)
        code = os.system(backup_cmd)
        if code == 0:
            Logger.warning(f'恢复[{db_path}]数据库执行成功！')
        else:
            Logger.error(f'恢复[{db_path}]数据库执行失败！（{code}）')

