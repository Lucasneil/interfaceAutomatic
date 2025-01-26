import logging

import yaml
import threading
from common.logger import Logger
from common.operation_excle import operation_excle
from pathlib import Path
import os


def write_config_all(obj):
    try:
        with open(ReadFile.config_path, 'r', encoding='utf-8') as file:
            data = yaml.load(file,Loader=yaml.FullLoader)
            print("原始数据:", data)
            data = obj
            print("配置修改后的数据:", data)
        with open(ReadFile.config_path, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, allow_unicode=True, default_flow_style=False)
            file.flush()
            os.fsync(file.fileno())
            print("全量配置写入成功")


    except yaml.YAMLError as ex:
        print(ex)


class ReadFile:
    def __init__(self, task_id=None):
        self.task_id = task_id
        self.config_path = (
            f"./config/config_{task_id}.yaml"
            if task_id
            else f"{str(Path(__file__).parent.parent)}/config/config.yaml"
        )
        self.config_dict = None  # 实例级配置缓存
    #config_dict = None
    #config_path = f"{str(Path(__file__).parent.parent)}/config/config.yaml"


    def get_config_dict(self):
        """读取当前任务的配置文件"""
        if self.config_dict is None:
            try:
                with open(self.config_path, "r", encoding="utf-8") as file:
                    self.config_dict = yaml.safe_load(file)
            except Exception as e:
                raise ValueError(f"加载配置文件失败: {e}")
        return self.config_dict



    def read_config(self, expr: str = "."):
        """从当前任务的配置中读取数据"""
        from common.exchange_data import ExchangeData
        config = self.get_config_dict()
        return ExchangeData.Extract_noe(config, expr)

    def write_config(self, obj):
        """将extra_pool写入当前任务的配置文件"""
        config = self.get_config_dict().copy()
        config['extra_pool'] = obj
        try:
            with open(self.config_path, 'w', encoding='utf-8') as file:
                yaml.dump(config, file, allow_unicode=True, default_flow_style=False)
        except Exception as e:
            raise IOError(f"写入配置文件失败: {e}")







    @classmethod
    def openpyxl_read_testcase(cls):
        """
        读取excel格式的测试用例,返回一个生成器对象
        :return 生成器
        """
        case_severity_list=ReadFile.read_config('$..case_severity')#获取测试用例级别

        excle_path = (cls.read_config("$.file_path.test_case"))#获取测试用例路径
        operation_excle_data=operation_excle.read_excel(excle_path, ['P1'] )  # 返回测试数据列表
        logging.debug("开始调用readFile里的operation_excle_data")
        return operation_excle_data


# 线程局部存储管理实例
_local = threading.local()

def get_readfile_instance(task_id=None):
    if not hasattr(_local, 'readfile'):
        _local.readfile = ReadFile(task_id)
    return _local.readfile



