from common.db import DB
from common.exchange_data import ExchangeData
import pytest,time
from common.logger import Logger
from common.read_file import ReadFile
from common.backup_recovery import BackupRecovery



#命令行传参addoption 在contetest.py添加命令行选项,命令行传入参数”—cmdopt“, 用例如果需要用到从命令行传入的参数，就调用cmdopt函数：
def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="test", help=None)

@pytest.fixture(scope='session',autouse=True)
def Acmdopt(pytestconfig):
    # 两种写法
    global  Acmdopt_env
    Acmdopt_env=pytestconfig.getoption("--env")
    return Acmdopt_env
    # return pytestconfig.option.cmdopt

@pytest.fixture(scope='session',autouse=True)
def env_url(Acmdopt):#读取配置文件拿到环境地址
    url = ReadFile.read_config('$.server.%s'%Acmdopt)#  $..test
    Logger.warning('执行环境为：【%s】 %s' %(Acmdopt_env,url))

    return [url,Acmdopt]
@pytest.fixture(scope='function',autouse=True)
def start_end():
    Logger.info("{:=^200s}".format("华丽的分割线【开始】"))
    yield
    Logger.info("{:=^200s}".format("华丽的分割线【结束】"))

@pytest.fixture(scope='session')  #读取数据库查询断言
def get_db(Acmdopt):
    assert_db = ReadFile.read_config('$.Operations_db.assert_db')
    db_info = dict(ReadFile.read_config('$.database.%s'%Acmdopt))
    if assert_db:#判断是否查询数据库断言
        db=DB(db_info)
    else:
        db=None

    yield db

    if assert_db:#判断是否查询数据库断言
        db.close()


#备份恢复数据库
@pytest.fixture(scope="session", autouse=True)
def bac_rec(Acmdopt):
    db_data = dict(ReadFile.read_config('$.database.%s'%Acmdopt))
    BR = BackupRecovery(db_data['data'])
    db_bak_path = './config/ry-vue_bak.sql'  # 当前数据库备份文件
    db_re_path = './config/ry-vue_re.sql'  # 初始化好测试数据的数据库sql文件
    backup = ReadFile.read_config('$.Operations_db.backup')
    if backup:
        BR.backup(db_bak_path)
        BR.recovery(db_re_path)
    yield
    recovery = ReadFile.read_config('$.Operations_db.recovery')
    if recovery:
        BR.recovery(db_bak_path)




def pytest_terminal_summary(terminalreporter):
    """
    收集测试结果
    """
    _PASSED = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    _ERROR = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    _FAILED = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    _SKIPPED = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    _TOTAL = terminalreporter._numcollected
    _TIMES = time.time() - terminalreporter._sessionstarttime
    Logger.info(f"用例总数: {_TOTAL}")
    Logger.success(f"通过用例: {_PASSED}")
    Logger.error(f"异常用例数: {_ERROR}")
    Logger.error(f"失败用例数: {_FAILED}")
    Logger.warning(f"跳过用例数: {_SKIPPED}")
    Logger.info(f"用例执行时长: {round(_TIMES, 2)} s")
    try:
        _RATE = _PASSED / _TOTAL * 100

        _SUCCESS_RATE=round(_RATE, 2)

    except ZeroDivisionError:
        _SUCCESS_RATE="0.00"
    Logger.info(f"用例成功率:{_SUCCESS_RATE}")
    result_data_test={
        "_TOTAL": f"{_TOTAL}",
        '_PASSED':f"{_PASSED}",
        "_ERROR": f" {_ERROR}",
        "_FAILED": f" {_FAILED}",
        "_SKIPPED": f" {_SKIPPED}",
        "_TIMES": f"{round(_TIMES, 2)} s",
        "_SUCCESS_RATE": f"{_SUCCESS_RATE}",
    }
    ExchangeData.post_pytest_summary(result_data_test)#测试结果添加到变量池
    with open("result.txt", "w") as fp:#测试结果保存到本地result.txt
        fp.write("_TOTAL=%s" % _TOTAL + "\n")
        fp.write("_PASSED=%s" % _PASSED + "\n")
        fp.write("_FAILED=%s" % _FAILED + "\n")
        fp.write("_ERROR=%s" % _ERROR + "\n")
        fp.write("_SKIPPED=%s" % _SKIPPED + "\n")
        fp.write("_SUCCESS_RATE=%.2f%%" % _SUCCESS_RATE + "\n")
        fp.write("_TIMES=%.2fs" % _TIMES)

# def pytest_itemcollected(item):#要不要这个函数都行 不用需要再用例的历史中看 ，  使用这个函数 所有执行全部显示处理
#     item._nodeid = str(random.randint(1, 1000)) + '_' + item . _nodeid