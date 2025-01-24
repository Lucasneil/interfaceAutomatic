from flask import Flask, request, jsonify, render_template
import logging
import pytest
import allure
from flask_assets import Environment, Bundle
from flask_socketio import SocketIO, emit, join_room
from contextlib import redirect_stdout
from common.rsa_encrypt import encrypt_data
import threading
import io
import yaml
import os
import run
from common.exchange_data import ExchangeData
from common.read_file import ReadFile
from common.public import ChangeVariables


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
run_lock = threading.Lock()


@app.route('/')
def test_index():
    return render_template('zszc_qy.html')
def change_conf(data):
    global case_dir
    #项目类型
    projectChoice = data.get("projectChoice")
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
    
    
    #根据传入的项目类型，匹配excel-case的路径
    if projectChoice == '涿州':
        case_dir = './data/env_test/case_excle/zz'
        print(case_dir)
    elif projectChoice == '产品化-三方':
        case_dir = './data/env_test/case_excle/sf'
    elif projectChoice == '产品化-企采':
        case_dir = './data/env_test/case_excle/qc'
    elif projectChoice == '金湡':
        case_dir = './data/env_test/case_excle/zz'
    elif projectChoice == '清苑':
        case_dir = './data/env_test/case_excle/zz'
    elif projectChoice == '无极':
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
    server = project_mapping.get(projectChoice)
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
    yaml_file_path = os.path.join(current_dir, '.', 'config', 'config.yaml')
    with open(yaml_file_path, 'r', encoding='utf-8') as f:
        yaml_data = yaml.load(f, Loader=yaml.FullLoader)
        # 通过页面传输的值替换字典中的值
        yaml_data['server']['test'] = server
        yaml_data['extra_pool']['url'] = server
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
        change_variables_instance = ChangeVariables()
        change_variables_instance.change_name_times(yaml_data['extra_pool'])
        print(yaml_data['server']['case_severity'])





        # 将替换完的字典写入yaml配置文件
    with open(yaml_file_path, 'w', encoding='utf-8') as f:
        yaml.dump(yaml_data, f,allow_unicode=True)
        f.flush()
        os.fsync(f.fileno())

def process_task(task_id,data):
    change_conf(data)
    ExchangeData.load_config()
    ReadFile.get_config_dict()


    f = io.StringIO()
    output = f.getvalue()
    with redirect_stdout(f):
        with run_lock:
            result = run.run()
        #print(result)
        logger.debug(result)

    # 更新任务状态
    task_status[task_id] = {
        'status': 'completed',
        'result': f'提交的数据已处理完成',
        'log': output
    }

    # 通过WebSocket发送日志
    socketio.emit('log', {'data': output}, room=task_id)



@app.route('/submit', methods=['POST'])
def test_submit():
    global task_id_counter
    data = request.form
    task_id = str(len(task_status) + 1)
    #task_id = str(len(task_status) + 1)
    #task_status[task_id] = {'status': 'processing', 'log': ''}
    task_status[task_id] = {'status': 'processing', 'log': ''}
    # 启动后台线程处理任务
    threading.Thread(target=process_task, args=(task_id,data)).start()
    #print("操作excel")

    return jsonify({'task_id': task_id})

@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    status = task_status.get(task_id, {'status': 'unknown'})
    return jsonify(status)
    pass

@socketio.on('join')
def on_join(data):
    task_id = data['task_id']
    join_room(task_id)
    pass


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000,threaded=True)
        # 执行run文件
