from datetime import datetime, timedelta
import time
import urllib
from urllib import parse
from common.exchange_data import ExchangeData

class ChangeVariables:

    def __init__(self, task_id=None):
        self.task_id = task_id
        # 获取当前任务的 extra_pool
        self.extra_pool = ExchangeData.get_extra_pool()
        # 其他初始化逻辑保持不变...
        self.dict_name_purchase = {'purchaseProjectName'}
        self.dict_name_section = {'bidSectionName1', 'bidSectionName2'}
        self.dict_name_decode = {'purchaseProjectNameDecode', 'bidSectionName1Decode', 'bidSectionName2Decode'}
        self.dict_time = {'bidDocReferEndTime', 'bidDocReferEndTimeCus', 'bidOpenTime', 'docGetEndTime', 'docGetEndTimeCus', 'noticeEndTime', 'noticeSendTime'}
    def func_por_name(self, object):
        try:
            tims = self.func_times(0)
            for key in self.dict_name_purchase:
                print("名称Key是" + str(key))
                if object == key:
                    va = '测试接口自动化项目'
                    return va + str(tims['datetimes'])
        except Exception as a:
            print("func_por_name异常：", a)

    def func_times(self, object: int) -> dict:
        try:
            if isinstance(object, int) and object >= 0:
                now = datetime.now()
                seconds_later = (now + timedelta(seconds=300)).replace(microsecond=0)
                one_day = timedelta(days=object)
                one_day_later = int((now + one_day).timestamp())
                datetimes = datetime.fromtimestamp(one_day_later)
                return {"one_day_later": str(one_day_later), "datetimes": datetimes, "seconds_later": seconds_later}
        except Exception as b:
            print("func_times异常:", b)

    def change_name_times(self, pool):
        pool['purchaseProjectName'] = self.func_por_name('purchaseProjectName')
        self.extra_pool['purchaseProjectName'] = pool['purchaseProjectName']
        
        # 更新标段名称
        self.extra_pool['bidSectionName1'] = f"{pool['purchaseProjectName']}-标段01"
        self.extra_pool['bidSectionName2'] = f"{pool['purchaseProjectName']}-标段02"
        print("替换完的名称值是" + str(pool['purchaseProjectName']))
        # 处理 URL 编码和解码逻辑
        for key in self.dict_name_decode:
            if key == 'purchaseProjectNameDecode':
                pool[key] = urllib.parse.quote(pool['purchaseProjectName'])
                self.extra_pool[key] = pool[key]
            elif key == 'bidSectionName1Decode':
                pool[key] = urllib.parse.quote(pool['bidSectionName1'])
                self.extra_pool[key] = pool[key]
            elif key == 'bidSectionName2Decode':
                pool[key] = urllib.parse.quote(pool['bidSectionName2'])
                self.extra_pool[key] = pool[key]

         # 处理时间参数
        for key in self.dict_time:
            if key == "noticeSendTime":
                pool[key] = str(self.func_times(20)['seconds_later'])
            else:
                pool[key] = str(self.func_times(20)['datetimes'])
            self.extra_pool[key] = pool[key]


