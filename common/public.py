from datetime import datetime, timedelta
import time
import urllib
from urllib import parse
from common.read_file import ReadFile
from common.exchange_data import ExchangeData

class ChangeVariables:

    def __init__(self):
        self.config = ExchangeData.extra_pool
        self.dict_name_purchase={'purchaseProjectName'}
        self.dict_name_section={'bidSectionName1','bidSectionName2'}
        self.dict_name_decode={'purchaseProjectNameDecode','bidSectionName1Decode','bidSectionName2Decode'}
        self.dict_time= {'bidDocReferEndTime', 'bidDocReferEndTimeCus', 'bidOpenTime', 'docGetEndTime', 'docGetEndTimeCus','noticeEndTime','noticeSendTime'}
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
        ExchangeData.extra_pool['purchaseProjectName'] = pool['purchaseProjectName']
        # 更新值
        ExchangeData.extra_pool['bidSectionName1'] = str(pool['purchaseProjectName']) + '-标段01'
        ExchangeData.extra_pool['bidSectionName2'] = str(pool['purchaseProjectName']) + '-标段02'
        print("替换完的名称值是" + str(pool['purchaseProjectName']))
        for key in pool.keys():
            if key in self.dict_name_decode and key=='purchaseProjectNameDecode':
                pool[key] = urllib.parse.quote(pool['purchaseProjectName'])
                ExchangeData.extra_pool[key] = pool[key]  # 更新值
                print("替换完的名称值是" + str(pool[key]))
            elif key in self.dict_name_decode and key=='bidSectionName1Decode':
                pool[key] = urllib.parse.quote(pool['bidSectionName1'])
                ExchangeData.extra_pool[key] = pool[key]  # 更新值
                print("替换完的名称值是" + str(pool[key]))
            elif key in self.dict_name_decode and key=='bidSectionName2Decode':
                pool[key] = urllib.parse.quote(pool['bidSectionName2'])
                ExchangeData.extra_pool[key] = pool[key]  # 更新值
                print("替换完的名称值是" + str(pool[key]))

            if key in self.dict_time:
                if key == "noticeSendTime":
                    pool[key] = str(self.func_times(20)['seconds_later'])
                    ExchangeData.extra_pool[key] = pool[key]  # 更新值
                    print(key + "的值是" + str(ExchangeData.extra_pool[key]))
                else:
                    pool[key] = str(self.func_times(20)['datetimes'])
                    ExchangeData.extra_pool[key] = pool[key]  # 更新值
                    print(key + "的值是" + str(ExchangeData.extra_pool[key]))


