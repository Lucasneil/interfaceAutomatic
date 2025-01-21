from faker import Faker
import time
from common.logger import Logger
fk = Faker("zh_CN")
import random
import requests
def uuid4():
    return fk.uuid4()

def Times():
    return fk.date_between_dates()


def list_random_index(lists_s):
    Logger.error(lists_s)
    Logger.error(type(lists_s))
    return random.randint(0,len(lists_s)-1)

def waits(t):

    time.sleep(t)
    Logger.warning('sleep %s s'%t)

    return 'sleep %s s'%t


def get_file_url(url):

    re=requests.request('get',url=url)
    status_code=re.status_code

    data_dic={
        "文件地址": url,
        "文件地址请求响应码":f'{status_code}(响应码)',

    }
    return data_dic

def edit_personal_info(extra_pool): #编辑个人信息参数

    user_info=extra_pool['user_info']
    user_info['avatar']=extra_pool['imgUrl']


    return extra_pool['user_info']

