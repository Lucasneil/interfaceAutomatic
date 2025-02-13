from flask import Flask, request, jsonify, render_template, send_from_directory
import logging
import pytest
import allure
from flask_assets import Environment, Bundle
from flask_socketio import SocketIO, emit, join_room
from contextlib import redirect_stdout
import subprocess
from common.read_exce_yaml_caes import get_yaml_excle_caes
from common.rsa_encrypt import encrypt_data
import threading
import io
import yaml
import os
import run
from common.exchange_data import ExchangeData
from common.read_file import ReadFile, get_readfile_instance
from common.public import ChangeVariables
import shutil
import uuid
import requests

app = Flask(__name__,template_folder='templates',static_folder='static',static_url_path='/static')
# 配置 logging 模块
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
assets = Environment(app)

# 初始化Flask-Assets
assets.url = app.static_url_path
assets.directory = app.static_folder



# 编译并注册scss_all bundle
scss_all = Bundle('scss/main.scss', output='css/main.css', filters='pyscss')
assets.register('scss_all', scss_all)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# 设置Flask jsonify返回中文不转码
app.json.ensure_ascii = False
yaml.allow_unicode = True

# 存储任务状态
task_status = {}

# 创建一个全局锁
#run_lock = threading.Lock()


@app.route('/')
def test_index():
    return render_template('zszc_qy.html')
def change_conf(data,task_id):
    global case_dir
    # 生成任务专属的配置文件路径
    temp_config_path = f'./config/config_{task_id}.yaml'
    shutil.copy('./config/config.yaml', temp_config_path)
    logging.debug(f"任务{task_id}的配置文件路径为：{temp_config_path}")
    #项目类型
    projectChoice = data.get("projectChoice")
    #项目类型：企采、政采、工程
    projectType = data.get("projectType")
    #招标人用户名和密码
    username = data.get("username")
    password = data.get("password")
    #print("招标人加密前")
    #print(password)
    password = encrypt_data(password)
    #print("招标人加密后")
    #print(password)
    #审批人用户名和密码
    firstAprUser = data.get("firstAprUser")
    firstAprPsw = data.get("firstAprPsw")
    #print("审批人加密前")
    #print(firstAprPsw)
    firstAprPsw = encrypt_data(firstAprPsw)
    #print("审批人密码加密后")
    #print(firstAprPsw)
    #采购方式
    purchaseMode = data.get('bidType')
    #招标组织形式，自行和委托
    tenderOrganizeForm = data.get('bidOrganization')
    #评标办法
    evaluation_method = data.get('evaluationMethod')
    #项目类型：货物、服务、工程
    purchaseProjectType = data.get('purchaseProjectType')
    #邀请方式：公开、邀请
    inviteType = data.get('inviteType')
    #资审方式：预审和后审
    pqrMode = data.get('pqrMode')
    #是否费用
    ifFee = data.get('ifFee')
    feeGuarantee = ''
    feeCash = ''
    feeCommitment = ''
    #保证金金额
    marginPrice = '0'
    #保证金单位
    marginUnit = '0'
    #文件费
    tfPrice = '0'
    #保证金缴纳方式
    guaranteeType = "" 
    proUrl = data.get('proUrl')
    logging.debug("proUrl传过来的值是" + proUrl)

    #根据传入的项目类型，匹配excel-case的路径
    if projectType == '企业采购':
        if projectChoice == '产品化-三方':
            case_dir = './data/env_test/case_excle/sf'
        elif projectChoice == '产品化-企采':
            case_dir = './data/env_test/case_excle/qc'
        else:
            case_dir = './data/env_test/case_excle/zz'
    if projectType == '政府采购':
        if projectChoice == '产品化-三方':
            case_dir = './data/env_test/case_excle/sf'
        elif projectChoice == '产品化-企采':
            case_dir = './data/env_test/case_excle/qc'
        else:
            case_dir = './data/env_test/case_excle/zz'
    if projectType == '工程建设':
        if projectChoice == '产品化-三方':
            case_dir = './data/env_test/case_excle/sf'
        elif projectChoice == '产品化-企采':
            case_dir = './data/env_test/case_excle/qc'
        else:
            case_dir = './data/env_test/case_excle/zz'
        


    #根据传入的招标文件信息做后续处理，根据传入的值进行相应转换
    ifSupportSmallMicro = data.get('ifSupportSmallMicro')
    print("app里的小微")
    print(ifSupportSmallMicro)
    if ifSupportSmallMicro == '1':
        ifSupportSmallMicro = "true"
        print("app里的小微")
        print(ifSupportSmallMicro)
    else:
        ifSupportSmallMicro = "false"
        print("app里的小微")
        print(ifSupportSmallMicro)
        
    ifJudgesConfirmWinBidder = data.get('ifJudgesConfirmWinBidder')
    print("是否评定分离")
    print(ifJudgesConfirmWinBidder)
    if ifJudgesConfirmWinBidder == '1':
        ifJudgesConfirmWinBidder = "true"
        print("是否评定分离")
        print(ifJudgesConfirmWinBidder)
    else:
        ifJudgesConfirmWinBidder = "false"
        print("是否评定分离")
        print(ifJudgesConfirmWinBidder)
    ifSupportBlindBid = data.get('ifSupportBlindBid')
    print("是否暗标")
    print(ifSupportBlindBid)
    if ifSupportBlindBid == '1':
        ifSupportBlindBid = "true"
        print("是否暗标")
        print(ifSupportBlindBid)
    else:
        ifSupportBlindBid = "false"
        print("是否暗标")
        print(ifSupportBlindBid)
    ifSyndicatedFlag = data.get('ifSyndicatedFlag')
    print("app里的小微")
    print(ifSyndicatedFlag)
    if ifSyndicatedFlag == '1':
        ifSyndicatedFlag = "true"
        print("app里的小微")
        print(ifSyndicatedFlag)
    else:
        ifSyndicatedFlag = "false"
        print("app里的小微")
        print(ifSyndicatedFlag)
    ifUseCa = data.get('ifUseCa')
    if  ifUseCa == '1':
        ifUseCa = "true"
        print("是否使用CA")
        print(ifUseCa)
    else:
        ifUseCa = "false"
        print("是否使用CA")
        print(ifUseCa)
    '''if  ifFee == '1':
        
        feeGuarantee = "1"
        feeCash = "2"
        feeCommitment = "3"
        marginPrice = "1"
        marginUnit = "1"
        tfPrice = "200"
    else:
        feeGuarantee = ""
        feeCash = ""
        feeCommitment = ""
        marginPrice = "0"
        marginUnit = "0"
        tfPrice = "0"
        '''
    #根据页面传入的【是否费用】的值来确定传参
    if ifFee == '1':
        print("有费用")
        ifFee = "1,2,3"
        guaranteeType = "1,2,3"
        marginPrice = "1"
        marginUnit = "1"
        tfPrice = "200"
    else:
        ifFee = ""
        guaranteeType = ""
        marginPrice = "0"
        marginUnit = "0"
        tfPrice = "0"
        

    # 项目选择字典
    project_mapping = {
        '产品化-三方': 'hhttp://trade.sanfang-test.zszc.jianshicha.cn/etbApi/',
        '涿州': 'http://trade.zz-test.zszc.jianshicha.cn/etbApi/',
        '产品化-企采': 'http://trade.sd-test.zszc.jianshicha.cn/api/',
        '金湡': 'http://trade.jy-test.zszc.jianshicha.cn/etbApi/',
        '清苑': 'http://trade.qy-test.zszc.jianshicha.cn/etbApi/',
        '无极': 'http://trade.wj-test.zszc.jianshicha.cn/etbApi/'

    }
    # 招标方式字典
    purchaseMode_mapping = {
        '公开招标': '1',
        '邀请招标': '2',
        '竞争性谈判': '3',
        '单一来源采购': '4',
        '询价采购': '5',
        '竞争性磋商': '6',
        '其他': '7'
    }
    # 招标组织形式字典
    tenderOrganizeForm_mapping = {
        '自行招标': '1',
        '委托招标': '2'
    }
    # 资审方式字典
    pqrMode_mapping = {
        '资格预审': '1',
        '资格后审': '2'
    }
    # 评标办法字典
    evaluation_method_mapping = {
        '最低评标价法': '1',
        '综合评标法': '2'
    }
    # 邀请方式字典
    inviteType_mapping = {
        '公开': '1',
        '邀请': '2'
    }
    purchaseProjectType_mapping = {
        '货物': 'D01',
        '服务': 'D03',
        '工程': 'D02'
   }
    # 匹配项目对应的测试地址
    if proUrl != '':
        logging.debug("proUrl不是空的")
        server = proUrl
        logging.debug(proUrl)
    else:
        logging.debug("proUrl是空的")
        server = project_mapping.get(projectChoice)
        logging.debug(server)

    # 匹配项目对应的招标方式、组织形式等
    purchaseMode = purchaseMode_mapping.get(purchaseMode)
    pqrMode = pqrMode_mapping.get(pqrMode)
    tenderOrganizeForm = tenderOrganizeForm_mapping.get(tenderOrganizeForm)
    evaluation_method = evaluation_method_mapping.get(evaluation_method)
    inviteType = inviteType_mapping.get(inviteType)
    print("邀请类型1是公开2是邀请")
    print(inviteType)
    purchaseProjectType = purchaseProjectType_mapping.get(purchaseProjectType)
    # print(inviteType + "inviteType")
    # 读取yaml配置文件为字典

    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    #yaml_file_path = os.path.join(current_dir, '.', 'config', 'config.yaml')
    with open(temp_config_path, 'r', encoding='utf-8') as f:
        yaml_data = yaml.load(f, Loader=yaml.FullLoader)
        # 通过页面传输的值替换字典中的值
        yaml_data['server']['test'] = server
        yaml_data['extra_pool']['url'] = server
        logging.debug("写入配置文件前的url是" + server)
        yaml_data['sheet_name'] = '1-招标-excle'
        yaml_data['extra_pool']['username'] = username
        yaml_data['extra_pool']['password'] = password
        yaml_data['extra_pool']['purchaseMode'] = purchaseMode
        yaml_data['extra_pool']['pqrMode'] = pqrMode
        yaml_data['extra_pool']['tenderOrganizeForm'] = tenderOrganizeForm
        yaml_data['extra_pool']['evaluation_method'] = evaluation_method
        yaml_data['extra_pool']['inviteType'] = inviteType
        yaml_data['test_case_type']['test'][0]['test_case'] = case_dir
        yaml_data['extra_pool']['firstAprUser'] = firstAprUser
        yaml_data['extra_pool']['firstAprPsw'] = firstAprPsw
        yaml_data['extra_pool']['ifSupportSmallMicro'] = ifSupportSmallMicro
        yaml_data['extra_pool']['ifJudgesConfirmWinBidder'] = ifJudgesConfirmWinBidder
        yaml_data['extra_pool']['ifSupportBlindBid'] = ifSupportBlindBid
        yaml_data['extra_pool']['ifSyndicatedFlag'] = ifSyndicatedFlag
        yaml_data['extra_pool']['ifUseCa'] = ifUseCa
        yaml_data['extra_pool']['ifFee'] = ifFee
        yaml_data['extra_pool']['guaranteeType'] = guaranteeType
        yaml_data['extra_pool']['purchaseProjectType'] = purchaseProjectType
        #yaml_data['extra_pool']['feeCash'] = feeCash
        #yaml_data['extra_pool']['feeCommitment'] = feeCommitment
        yaml_data['extra_pool']['marginPrice'] = marginPrice
        yaml_data['extra_pool']['marginUnit'] = marginUnit
        yaml_data['extra_pool']['tfPrice'] = tfPrice
        change_variables_instance = ChangeVariables(task_id=task_id)
        change_variables_instance.change_name_times(yaml_data['extra_pool'])
        print(yaml_data['server']['case_severity'])





        # 将替换完的字典写入yaml配置文件
    with open(temp_config_path, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f, allow_unicode=True)
        return temp_config_path
    

def process_task(task_id, data):
    ExchangeData.load_config(task_id)
    # 1. 生成任务专属配置文件
    temp_config_path = change_conf(data, task_id)  # 修改后的 change_conf 返回临时路径
    # 2. 加载配置到当前线程的 ExchangeData
    extra_pool = ExchangeData.load_config(task_id)
    username = extra_pool['username']
    password = extra_pool['password']
    firstAprUser = extra_pool['firstAprUser']
    firstAprPsw = extra_pool['firstAprPsw']
    url = extra_pool['url'] + 'etbuser/login'
    logging.debug("页面调用登录接口时的URL是" + url)
    data1 = {"username" : username,"password" : password, "identity": "1"}
    data2 = {"username" : firstAprUser,"password" : firstAprPsw, "identity": "1"}
    response1 = requests.post(url = url, json = data1)
    logging.debug(response1.json())
    responseUser = response1.json().get('msg')
    logging.debug(responseUser)

    if responseUser == "登录成功" and firstAprUser != '':
        logging.debug("招标人登录成功")
        response2 = requests.post(url = url, json = data2)
        logging.debug(response2.json())
        responseAppr = response2.json().get('msg')
        logging.debug(responseAppr)
        if responseAppr == "登录成功":
            # 3. 执行测试
            f = io.StringIO()
            output = f.getvalue()
            with redirect_stdout(f):
                # with run_lock:
                result = run.run(task_id)
                # print(result)
                logger.debug(result)

            # 生成 Allure 报告
            report_dir = f'./target/allure-results_{task_id}'
            report_output_dir = f'./static/allure-report_{task_id}'  # 将报告放在静态文件目录中
            os.makedirs(report_output_dir, exist_ok=True)
            allure_command = ['allure', 'generate', report_dir, '-o', report_output_dir, '--clean']
            subprocess.run(allure_command, check=True)

            # 更新任务状态
            task_status[task_id] = {
                'status': 'completed',
                'result': f'提交的数据已处理完成',
                'log': output,
                'report_url': f'/allure-report/{task_id}/index.html'  # 添加报告 URL
            }

            # 通过WebSocket发送日志
            socketio.emit('log', {'data': output}, room=task_id)
        else:
            # 更新任务状态
            task_status[task_id] = {
                'status': 'completed',
                'result': f'审批人用户名或密码错误'
            }
    elif responseUser == "登录成功" and firstAprUser == '':
        # 3. 执行测试
        f = io.StringIO()
        output = f.getvalue()
        with redirect_stdout(f):
            # with run_lock:
            result = run.run(task_id)
            # print(result)
            logger.debug(result)

        # 生成 Allure 报告
        report_dir = f'./target/allure-results_{task_id}'
        report_output_dir = f'./static/allure-report_{task_id}'  # 将报告放在静态文件目录中
        os.makedirs(report_output_dir, exist_ok=True)
        allure_command = ['allure', 'generate', report_dir, '-o', report_output_dir, '--clean']
        subprocess.run(allure_command, check=True)

        # 更新任务状态
        task_status[task_id] = {
            'status': 'completed',
            'result': f'提交的数据已处理完成',
            'log': output,
            'report_url': f'/allure-report/{task_id}/index.html'  # 添加报告 URL
        }
    else:
        # 更新任务状态
        task_status[task_id] = {
            'status': 'completed',
            'result': f'招标人用户名或密码错误'
        }



@app.route('/submit', methods=['POST'])
def test_submit():
    #global task_id_counter

    task_id = str(uuid.uuid4())  # 生成唯一任务ID
    data = request.form
    # 获取当前请求的 host（例如 http://192.168.1.100:5000）
    host = request.host_url  # 或者 request.url_root
    # #task_id = str(len(task_status) + 1)
    #task_status[task_id] = {'status': 'processing', 'log': ''}
    task_status[task_id] = {'status': 'processing', 'log': ''}
    temp_config_path = f'./config/config_{task_id}.yaml'
    shutil.copy('./config/config.yaml', temp_config_path)
    # 启动后台线程处理任务
    # 将 host 传递给 process_task
    threading.Thread(target=process_task, args=(task_id, data, host)).start()
    
    #print("操作excel")

    return jsonify({'task_id': task_id})

@app.route('/static/allure-report/<task_id>/<path:filename>')
def serve_allure_report(task_id, filename):
    report_dir = f'./static/allure-report_{task_id}'
    return send_from_directory(report_dir, filename)

@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    status = task_status.get(task_id, {'status': 'unknown'})
    return jsonify(status)


@socketio.on('join')
def on_join(data):
    task_id = data['task_id']
    join_room(task_id)
    pass


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
        # 执行run文件
