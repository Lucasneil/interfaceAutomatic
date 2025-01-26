import logging

from common.read_file import get_readfile_instance
import os
from common.operation_excle import operation_excle
from common.logger import Logger
import threading
from common.exchange_data import ExchangeData

def get_yaml_all_caes(yaml_file,task_id=None):  # 获取yaml文件中的所有用例
    _thread_local = threading.local()
    task_id = _thread_local.task_id
    logging.debug(f"readexcel里的taskid是: {task_id}")
    readfile = get_readfile_instance(task_id)
    get_all_yaml = readfile.read_config(yaml_file)  # 获取存放yaml文件目录路径
    case_severity_list = readfile.read_config('$..case_severity')
    yaml_path_all = []  # 收集所有的yaml文件路径

    for i in os.listdir(get_all_yaml):
        if (i.endswith(('yaml'))):
            yaml_path_all.append(os.path.join(get_all_yaml, i))

    all_yaml_case = []  # 收集所有用例
    for one_caselist_path in yaml_path_all:
        title = one_caselist_path.split('/')[-1].split('.')[0]
        for one_case in readfile.read_config(one_caselist_path):
            (one_case.insert(0, title))  # .insert(0,title)
            if one_case[5] in case_severity_list:  # 筛选匹配的用例等级进行测试
                all_yaml_case.append(one_case)

    return all_yaml_case


def get_excle_all_caes(excle_file, task_id=None):  # 获取excle文件中的所有用例
    """获取Excel用例（适配任务ID）"""

    task_id =ExchangeData.get_task_id()
    logging.debug(f"readexcel里的taskid是: {task_id}")
    readfile = get_readfile_instance(task_id)
    #config = readfile.read_config(task_id)
    get_all_excle = readfile.read_config(excle_file)  # 获取存放excle文件目录路径
    print("获取get_all_excle")
    print(get_all_excle)

    excle_path_all = []  # 收集所有的excle文件路径
    print(excle_path_all)

    for i in os.listdir(get_all_excle):
        if (i.endswith(('xlsx', 'xls'))):
            excle_path_all.append(os.path.join(get_all_excle, i))

    all_excle_case = []  # 收集所有用例
    a=0
    for one_excle_path in excle_path_all:
        a=a+1
        print("执行循环的次数是")
        print(a)
        print(one_excle_path, "路径")
        print(excle_path_all, "all路径")
        try:
            print("开始调用read——excel里的operation")
            #data = ConfigLoader.load_config()
            inviteType = readfile.read_config('$..inviteType')
            #inviteType = ReadFile.read_config('$..inviteType')
            logging.debug("read-excel里读取到的inviteType")
            logging.debug(inviteType)
            one_excle_case = operation_excle.read_excel(one_excle_path,['P1'],inviteType)
        except Exception as e:
            Logger.warning('这个文件【%s】无法读取,原因:“%s”,关闭excle再试试…… ' % (one_excle_path, e))
            one_excle_case = []
        all_excle_case = all_excle_case + one_excle_case

    return all_excle_case


def get_yaml_excle_caes(cmdopt_env='test', task_id=None):  # get_all_yaml_excle_caes  #获取yaml和excle用例，用例；yaml和excle累计所有
    # cmdopt_env='test'
    # Logger.error(cmdopt_env)
    """整合YAML和Excel用例（适配任务ID）"""
    task_id = ExchangeData.get_task_id()
    readfile = get_readfile_instance(task_id)
    test_case_type = (readfile.read_config('$.test_case_type.%s' % cmdopt_env))
    #print(test_case_type)
    # test_case_type = (ReadFile.read_config('$.test_case_type' ))

    test_case_type = sorted(test_case_type, key=lambda test_case_type: test_case_type['order'], reverse=False)

    all_yaml_xlsx_caes = []
    b=0
    for case_type in test_case_type:
        b=b+1
        print("case_type的循环次数")
        print(b)
        print("caseType的值是")
        print(case_type)
        print("test_case_type的值是")
        print(test_case_type)
        if case_type["read"]:
            print("符合第一个if")
            if case_type['file'] == "yaml":
                print("符合第二个if")
                all_yaml_xlsx_caes = all_yaml_xlsx_caes + get_yaml_all_caes(case_type['test_case'])
            elif case_type['file'] == "xlsx":
                print("符合第三个if")
                all_yaml_xlsx_caes = all_yaml_xlsx_caes + get_excle_all_caes(case_type['test_case'])
                print(all_yaml_xlsx_caes, "取出来的excel数据")

    return all_yaml_xlsx_caes
