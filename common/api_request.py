import time
import requests
import yaml
from common.condition import Condition
from common.logger import Logger
from common.exchange_data import ExchangeData
import allure, json, re
from common.read_file import ReadFile, get_readfile_instance  # 导入 get_readfile_instance
from common.public import ChangeVariables


class Api_Request():
    @classmethod
    def api_data(cls, cases, env_url):
        (
            case_mod,
            case_id,
            case_title,
            header_ex,
            path,
            case_severity,
            skips,
            method,
            parametric_key,
            file_obj,
            data,
            extra,
            sql,
            expect,
            latency_time,
        ) = cases
        Logger.info(f'用例名称：{case_mod}-{case_id}-{case_title}')
        allure.dynamic.story(case_mod)
        time.sleep(1)
        Condition().skip_if(cases)

        url, env = env_url  # 环境，url
        extra_pool = ExchangeData.get_extra_pool()  # 使用 get_extra_pool 方法
        extra_pool.update({
            "url": url,
            "env": env,
        })

        read_file = get_readfile_instance()  # 获取 ReadFile 实例
        allure.dynamic.severity(read_file.read_config('$..cor_rel_case_severity')[case_severity])

        request_headers = str(read_file.read_config('$.request_headers'))  # 获取配置文件中的请求头
        request_parameters = str(read_file.read_config('$.request_parameters'))  # 获取配置文件中的请求参数
        extra_pool = read_file.read_config('$.extra_pool')

        case_title = ExchangeData.rep_expr(case_title, return_type='srt')
        path = ExchangeData.rep_expr(path, return_type='srt')
        header_ex = ExchangeData.rep_expr(header_ex, return_type='dict')
        request_headers = ExchangeData.rep_expr(request_headers, return_type='dict')
        data = ExchangeData.rep_expr(data, return_type='dict')
        file_obj = ExchangeData.rep_expr(file_obj, return_type='dict')
        request_parameters = ExchangeData.rep_expr(request_parameters, return_type='dict')

        header_ex.update(request_headers)  # 合并配置文件中请求头
        if type(data) is dict:
            data.update(request_parameters)  # 合并配置文件中请求参数

        print("更新完成后的参数是" + str(data))

        allure.dynamic.title(case_title)

        pattern = re.compile(r'^((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+')
        if (pattern.search(path)) == None:  # 判断读取的地址是否有前缀地址http://192.168.1.153:8562
            if url[-1] == '/':
                url = url[:-1]
            urls = "%s/%s" % (url, path)  # 无前缀读取配置文件添加前缀
        else:
            urls = path  # 有前缀使用读取的完整地址

        allure.dynamic.description(
            "【用例名称】：%s_%s\n\n【请求地址】：%s\n\n【请求参数】：%s" % (case_mod, case_title, urls, data))
        proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

        # 使用代理方式
        res = Api_Request().api_request(urls, proxies, method, parametric_key, header_ex, (data), file_obj)
        # 不使用代理方式
        # res = Api_Request().api_request(urls, method, parametric_key, header_ex, (data), file_obj)
        print('test')
        if cases[-1]:
            print('等待时间')
            time.sleep(6)
        ExchangeData.Extract(res, extra)

        print(res, 'wjj11111')
        return res

    def api_request(self, url, proxies, method, parametric_key, header=None, data=None, file_obj=None) -> dict:
        if parametric_key == "params":
            parametric = {"params": data}
        elif parametric_key == "data":
            parametric = {"data": data}
        elif parametric_key == "json":
            parametric = {"json": data}
        else:
            raise ValueError("“parametric_key”的可选关键字为params, json, data")
        print(type(parametric), '测试测试测试测试')
        print(parametric)

        if file_obj != {}:
            file_objs = {}
            for k, v in file_obj.items():
                file_objs[k] = open(v, 'rb')
        else:
            file_objs = {}

        req_info = {
            "请求地址": url,
            "请求头": header,
            "请求方法": method,
            '参数类型': parametric_key,
            "请求数据": data,
            "上传文件": file_obj,
        }

        with allure.step('请求数据：'):
            allure.attach(
                json.dumps(req_info, ensure_ascii=False, indent=4),
                "附件内容",
                allure.attachment_type.JSON,
            )

        Logger.info('接口地址：%s' % url)
        Logger.info('请求头：%s' % header)
        Logger.info('请求方法：%s' % method)
        Logger.info('参数类型：%s' % parametric_key)
        Logger.info('请求参数：%s' % data)
        Logger.info('上传文件：%s' % file_obj)
        read_file = get_readfile_instance()  # 获取 ReadFile 实例
        print(read_file.read_config('$.request_parameters'), 'config.基准参数')
        proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

        try:
            if method == "WS":
                print("开始WS请求")
                res = websocket_run()
                time.sleep(10)
                print("ws请求成功")
                print(res)
            else:
                # 使用代理方便burpsuite抓取请求
                '''res = requests.request(method=method, url=url, proxies=proxies, headers=header, files=file_objs,
                                      **parametric)  # files=file,'''
                # 不使用代理
                res = requests.request(method=method, url=url,  headers=header, files=file_objs,
                                       **parametric)  # files=file,
                response = res.json()
        except Exception as e:
            Logger.error('请求发送失败：%s' % ((e)))
            response = {'response': str(e)}
            # ReadFile.write_config('config.yaml', ExchangeData())

        Logger.info('返回响应：%s' % response)

        with allure.step('响应数据：'):
            allure.attach(
                json.dumps(response, ensure_ascii=False, indent=4),
                "附件内容",
                allure.attachment_type.JSON,
            )

        return response