import sys
import requests
import time


class SendNotice():
    def __init__(self):

        self.JOB_URL = sys.argv[1]
        self.JOB_NAME = sys.argv[2]
        self.BUILD_NUMBER = sys.argv[3]
        self.CHANGES_SINCE_LAST_SUCCESS = sys.argv[4]
        self.SERVES_URL = sys.argv[5]

        try:
            self.SERVES_URL = sys.argv[5]
            self.URL_all = '服务地址：（AFS）\n'
            n = 1
            for URL in self.SERVES_URL.split(','):
                if URL != '':
                    self.URL_all = self.URL_all + f'{n}.{URL}\n'
                    n += 1
        except:
            self.URL_all = ''

        with open(f'result.txt', encoding='utf-8') as file:
            content = file.read()
            self.tetx = (content.rstrip())  ##rstrip()删除字符串末尾的空行
            self.tetx = self.tetx.replace('_TOTAL', '1.用例总数').replace('_PASSED', '2.用例通过数').replace('_FAILED',
                                                                                                             '3.用例失败数').replace(
                '_ERROR', '4.用例异常数').replace('_SKIPPED', '5.用例跳过数').replace('_SUCCESS_RATE',
                                                                                      '6.用例通过率').replace('_TIMES',
                                                                                                              '7.执行时长')
            self.tetx = self.tetx.replace('=', '：')
            self.tetx = f"用例测试概况：（AFS）\n{self.tetx}"
        #     for i in tetx.split('\n'):
        #         if i !='':
        #             i=i.split('=')
        #
        #             result_dic[i[0]]=i[1]
        # print(tetx)

        self.currenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.url = sys.argv[6]  # 'https://open.feishu.cn/open-apis/bot/v2/hook/2d0b6357-333a-4077-9fcd-61e361a3e51e'
        self.method = 'post'
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.json = {
            "msg_type": "interactive",
            "card": {
                "config": {
                    "wide_screen_mode": True,
                    "enable_forward": True
                },
                "elements": [{
                    "tag": "div",
                    "text": {
                        "content": "项目名称：" + self.JOB_NAME + "\n构建编号：第" + self.BUILD_NUMBER + "次构建\n测试时间：" + self.currenttime + '\n' + self.URL_all + '\n' + self.tetx,
                        "tag": "lark_md"
                    }
                }, {
                    "actions": [{
                        "tag": "button",
                        "text": {
                            "content": "查看报告",
                            "tag": "lark_md"
                        },
                        "url": self.JOB_URL,
                        "type": "default",
                        "value": {}
                    }],
                    "tag": "action"
                }],
                "header": {
                    "title": {
                        "content": self.JOB_NAME + " 构建报告",
                        "tag": "plain_text"
                    }
                }
            }
        }

    def send_feishu(self):
        requests.request(method=self.method, url=self.url, headers=self.headers, json=self.json)


if __name__ == '__main__':
    SendNotice().send_feishu()
