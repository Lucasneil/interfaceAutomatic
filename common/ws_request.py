from datetime import time
from common.read_file import ReadFile
import requests
import websocket
from websocket import WebSocketApp

from common.exchange_data import ExchangeData
import time
import threading

import json
import re

token = ReadFile.get_config_dict()['extra_pool']['token']
# print(token)
sectionId = ReadFile.get_config_dict()['extra_pool']['bidSectionId']
def extract_steps(message):
    # 使用正则表达式提取包含 JSON 数据的部分
    json_match = re.search(r'(\{.*\})', message)
    if not json_match:
        print("未找到 JSON 数据")
        return {}

    json_data = json_match.group(1)
    print("提取到的 JSON 数据:", json_data)
    json_data = json_data.replace('\\"', '"').replace('\\\\', '\\')

    # 解析外层的 JSON 数据
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError:
        print("外层 JSON 解码失败")
        return {}

    # 提取 content 字段中的数据
    try:
        content_str = data["data"]["content"]
        print("原始 content 字符串:", content_str)

        # 去除 content 字符串中的转义字符（\\）
        content_data_str = content_str.split('|')[2]  # 获取 JSON 字符串部分
        content_data_str = content_data_str.replace(r'\\', r'')  # 去除转义字符
        print("去除转义字符后的 content 字符串:", content_data_str)

        # 解析去掉转义字符后的 JSON 数据
        content_data = json.loads(content_data_str)
        print("解析后的 content 数据:", content_data)
        result = {step['stepName']: step['stepId'] for group in content_data for step in group['stepList']}

    except (json.JSONDecodeError, IndexError, AttributeError) as e:
        print("解析步骤信息时出错:", e)
        return {}

    return result


def afterws_request():

    # print(sectionId)
    url = 'http://kaiping.qy-test.zszc.jianshicha.cn/etbApi/etb-eval/tpEvalResult/initEvalStepList?sectionId=sectionId1&hallFlag=1'
    url1 = url.replace('sectionId1', sectionId)
    print(url1)
    token1 = 'Bearer ' + token
    identity1 = 'IdentityRole_1'
    # print(token1)
    headers = {
        'identityRole': identity1,
        'Authorization': token1,
    }
    # print(headers)
    res = requests.get(url=url1, headers=headers)
    # print(res)
    res1 = json.loads(res.text)
    # print(res1)
    res2 = res1['msg']
    # print(res2)
    if res1['msg'] == '操作成功!':
        print("发起http请求成功")
    else:
        print("发起请求失败" + res.text)


def on_open(wsapp):
    print("on_open")

    def send_message():
        se2 = "SUBSCRIBE\nid:sub-1\ndestination:/topic/group.WS101sectionId\n\n\u0000"
        se22 = se2.replace('sectionId',sectionId)
        send1 = ["CONNECT\nuserId:1849011030244642816\naccept-version:1.2,1.1,1.0\nheart-beat:0,8000\n\n\u0000"]
        #send2 = ["SUBSCRIBE\nid:sub-1\ndestination:/topic/group.WS1011853984361870467074\n\n\u0000"]
        send2 = [se22]
        wsapp.send(json.dumps(send1))
        time.sleep(1)
        wsapp.send(json.dumps(send2))

    threading.Thread(target=send_message).start()


def on_data(wsapp, frame_data, frame_opcode, frame_fin):
    print("on_data", frame_data, frame_opcode, frame_fin, sep=", ")


def on_message(wsapp, data):
    print("on_message", data, sep=", ")

    if 'nsubscription:sub-1' in data:
        print("存在")

        other_req = afterws_request()
        # 将 WebSocket 返回的数据去掉无用字符
        data_cleaned = data.strip()[2:-1]  # 去掉最外层的 '[' 和 ']'，如果有的话
        print("Cleaned data:", data_cleaned)
        if 'stepId' in data_cleaned:
            step_ids = extract_steps(data_cleaned)
            # 打印 step_ids 确认输出
            print("Extracted step IDs:", step_ids)
            stepid1 = step_ids['测试']
            stepid2 = step_ids['汇总评审结果']
            stepid3 = step_ids['评标报告确认']
            stepid4 = step_ids['评审结果签字']
            print("第一个步骤ID是" + stepid1, stepid2, stepid3, stepid4)
            ExchangeData.extra_pool['stepId1'] = stepid1
            ExchangeData.extra_pool['stepId2'] = stepid2
            ExchangeData.extra_pool['stepId3'] = stepid3
            ExchangeData.extra_pool['stepId4'] = stepid4
            print(ExchangeData.extra_pool)
            ReadFile.write_config(ExchangeData.extra_pool)


def on_cont_message(wsapp, frame_data, frame_fin):
    print("on_cont_message", frame_data, frame_fin, sep=", ")


def on_ping(wsapp, frame_data):
    print("on_ping", frame_data, sep=", ")
    # 接收到 PING 数据帧后, 需要立即给服务端回复 PONG 数据帧


def on_pong(wsapp, frame_data):
    print("on_pong", frame_data, sep=", ")
    wsapp.send("SUBSCRIBE\nid:sub-1\ndestination:/topic/group.WS1011853984361870467074\n\n\u0000",
               websocket.ABNF.OPCODE_PONG)


def on_error(wsapp, e):
    print("on_error", e, sep=", ")


def on_close(ws, close_status_code, close_reason):
    print("Connection closed:", close_status_code, close_reason)


def websocket_run():
    wsapp = WebSocketApp("ws://kaiping.qy-test.zszc.jianshicha.cn/etbApi/im/websocket/430/oeadovb5/websocket",
                         on_open=on_open,
                         on_data=on_data,
                         on_message=on_message,
                         on_cont_message=on_cont_message,
                         on_ping=on_ping,
                         on_pong=on_pong,
                         on_error=on_error
                         )

    wsapp.run_forever(ping_interval=2, ping_timeout=1 )


if __name__ == '__main__':
     websocket_run()
