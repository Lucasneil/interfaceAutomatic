#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# @Time    : 2022/8/18 20:42
# @Author  : mojin
# @Email   : 397135766@qq.com
# @File    : run.py
# @Software: PyCharm
#-------------------------------------------------------------------------------


import requests
from requests_toolbelt import MultipartEncoder
def hy_files():
    url='http://192.168.1.234:8056/prod-api/system/user/profile/avatar' # 传图片
    headers={
        "authorization": "eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6ImVlMjNkZDRjLWVkYmItNGNkYy1iYTkxLTc1YmMxZGI2ZTFkZSJ9.NviR_Hp23HbiMtsQr-95n64IBvIHcSMQrSZCVZRwRVzb3EXyNLJAikPqCd2ylCHtHvtri2C3Ya9l46rnyvnHdw",

    }
    data = MultipartEncoder(
        fields={
            "avatarfile": ('1.jpg',
                             open('./config/1.jpg', 'rb'),
                             "image/png")
        }
    )
    headers["Content-Type"] = data.content_type
    print(headers)
    print(data)
    r=requests.request(url=url,method='post',headers=headers,data=data)#,data=data
    print(r.text)

hy_files()
def hy_files2():
    url='http://192.168.1.234:8056/prod-api/system/user/profile/avatar' # 传图片
    headers={
        "authorization": "eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6ImVlMjNkZDRjLWVkYmItNGNkYy1iYTkxLTc1YmMxZGI2ZTFkZSJ9.NviR_Hp23HbiMtsQr-95n64IBvIHcSMQrSZCVZRwRVzb3EXyNLJAikPqCd2ylCHtHvtri2C3Ya9l46rnyvnHdw",

    }
    files = {
        "avatarfile": ('1.jpg', open('./config/1.jpg', "rb"), "avatarfile")
    }

    files = {
        'avatarfile': open('./config/1.jpg', 'rb'),
    }

    data={}
    print(headers)
    #print(data)
    r=requests.request(url=url,method='post',headers=headers,data=data,files=files)#,data=data
    print(r.text)

hy_files2()