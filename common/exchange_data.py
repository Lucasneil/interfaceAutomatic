import jsonpath
import re
import allure
import json
from faker import Faker
from string import Template
from yaml import Loader
from common.logger import Logger
from common.hook import *
from common.read_file import ReadFile
import yaml
import os
from pathlib import Path
import threading
class ExchangeData:
    _thread_local = threading.local()
    @staticmethod
    def read_config_file(yaml_file_path):
        with open(yaml_file_path, 'r', encoding='utf-8') as f:
            yaml_data = yaml.load(f, Loader=yaml.FullLoader)
        return yaml_data


    @classmethod
    def get_extra_pool(cls):
        """获取当前线程的 extra_pool"""
        if not hasattr(cls._thread_local, 'extra_pool'):
            # 初始化空字典
            cls._thread_local.extra_pool = {}
        return cls._thread_local.extra_pool

    @classmethod
    def set_extra_pool(cls, config):
        """设置当前线程的 extra_pool"""
        cls._thread_local.extra_pool = config.copy()

    @classmethod
    def load_config(cls,task_id):
        cls._thread_local.task_id = task_id
        config_path = f"./config/config_{task_id}.yaml"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                # 更新当前线程的 extra_pool
                cls.set_extra_pool(config.get('extra_pool', {}))
                
                print("通过exchangeData读取到的配置是")
                print(cls.get_extra_pool())
                extra_pool = cls._thread_local.extra_pool
                return extra_pool
        except Exception as e:
            raise ValueError(f"Failed to load config for task {task_id}: {e}")

    @classmethod
    def get_task_id(cls):
        """获取当前线程的 task_id"""
        if not hasattr(cls._thread_local, 'task_id'):
            raise AttributeError("task_id is not set in the current thread")
        return cls._thread_local.task_id
    @classmethod
    def Extract(cls, response, json_path_dic):
        """从响应中提取参数到当前线程的 extra_pool"""
        current_pool = cls.get_extra_pool()
        try:
            if json_path_dic:
                for k, v in eval(json_path_dic).items():
                    v = cls.rep_expr(v, return_type='no')
                    jsonpath_v = jsonpath.jsonpath(response, v)
                    if jsonpath_v:
                        current_pool[k] = jsonpath_v[0]  # 提取第一个匹配值
        except Exception as e:
            pass  # 可根据需要添加日志

    @classmethod
    def Extract_noe(cls, dic_data, josn_path):  # 提取参数return出去
        josn_path = cls.rep_expr(josn_path, return_type='no')

        try:
            Extract_noe_v_list = jsonpath.jsonpath(dic_data, josn_path)
            Extract_noe_v = Extract_noe_v_list[random.randint(0, len(Extract_noe_v_list) - 1)]  # 如拿到是多个数据，列表，随机取其中一个
        except Exception as e:
            Extract_noe_v = josn_path

        return Extract_noe_v

    @classmethod
    def exec_func(cls, func: str) -> str:
        """执行函数(exec可以执行Python代码)
        :params func 字符的形式调用函数
        : return 返回的将是个str类型的结果
        """
        loc = locals()
        exec(f"result = {func}")
        return str(loc['result'])

    @classmethod
    def rep_expr(cls, content: str, return_type='srt'):
        """从请求参数的字符串中，使用正则的方法找出合适的字符串内容并进行替换
        :param content: 原始的字符串内容
        :param return_type: 返回值类型 srt   dict   no 不改变类型
        return content： 替换表达式后的字符串
        """
        """替换表达式中的变量，基于当前线程的 extra_pool"""
        current_pool = cls.get_extra_pool()
        if not isinstance(content, int):  # 判断传来的值为int,直接跳出，否则报错 return self.pattern.sub(convert, self.template) E TypeError: expected stri
            if content != "":
                #data = cls.extra_pool
                try:
                    content = Template(content).safe_substitute(current_pool)
                except:
                    content = content
                try:
                    for func in re.findall('\\${(.*?)}', content):  # ${sdsd()} '\\${(.*?)}'
                        content = content.replace('${%s}' % func, cls.exec_func(func))
                except:
                    content = content
            else:  # 如果为空，
                pass  # 如果为空，则content=content 或pass(这两种一样的性质)
            # 判断返回类型
            if return_type == "srt":
                content = (content)
            elif return_type == "dict":  # 如果返回为字典
                if content == "":  # 判断是否为值
                    content = "{}"  # 为空值赋值字符串类的空字典

                try:  # 尝试转为字典类型
                    content = eval(content)  # “{}”转成功了{}
                except Exception as e:  # 字符串格式转字典异常情况
                    Logger.warning(content)
                    Logger.warning("Excle输入的字符串格式，不能转为字典类型， 请检查参数!!!(%s)" % str(e))
                    raise Exception("Excle输入的字符串格式，不能转为字典类型，请检查参数!!!(%s)" % str(e))
            elif return_type == "no":  # 如果为no  不转类型
                content = content

        return content



    @classmethod
    def post_pytest_summary(cls, result_data_test):
        """更新当前线程的 extra_pool"""
        current_pool = cls.get_extra_pool()
        #readfile = ReadFile(task_id=os.environ.get("CURRENT_TASK_ID"))
        current_pool.update(result_data_test)
        project_name = current_pool['purchaseProjectName']
        current_pool.update({"PROJECT_NAME": project_name})

    @classmethod
    def get_pytest_summary(cls):  # 读取report.html模板，替换变量后，返回完整的html 作为发送邮件内容
        file = open('./config/report.html', "r", encoding="utf-8")
        data = file.read()
        file.close()
        data = ExchangeData.rep_expr(data, return_type='srt')
        return data

    @classmethod
    def merging_dic(cls, *dict_list):  # 合并字典数据
        dic_date = {}
        for i in dict_list:
            dic_date.update(cls.extra_pool[i])
        return dic_date

