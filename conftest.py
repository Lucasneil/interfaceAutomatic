from common.db import DB
from common.exchange_data import ExchangeData
import pytest, time
from common.logger import Logger
from common.read_file import ReadFile, get_readfile_instance  # 导入 get_readfile_instance
from common.backup_recovery import BackupRecovery

# 命令行传参 addoption 在 conftest.py 添加命令行选项, 命令行传入参数”—cmdopt“, 用例如果需要用到从命令行传入的参数，就调用 cmdopt 函数：
def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="test", help=None)

@pytest.fixture(scope='session', autouse=True)
def Acmdopt(pytestconfig):
    # 两种写法
    global Acmdopt_env
    Acmdopt_env = pytestconfig.getoption("--env")
    return Acmdopt_env
    # return pytestconfig.option.cmdopt

@pytest.fixture(scope='session', autouse=True)
def env_url(Acmdopt):  # 读取配置文件拿到环境地址
    read_file = get_readfile_instance()  # 获取 ReadFile 实例
    url = read_file.read_config('$.server.%s' % Acmdopt)  # 使用实例调用 read_config
    Logger.warning('执行环境为：【%s】 %s' % (Acmdopt_env, url))

    return [url, Acmdopt]

@pytest.fixture(scope='function', autouse=True)
def start_end():
    Logger.info("{:=^200s}".format("华丽的分割线【开始】"))
    yield
    Logger.info("{:=^200s}".format("华丽的分割线【结束】"))

@pytest.fixture(scope='session')  # 读取数据库查询断言
def get_db(Acmdopt):
    read_file = get_readfile_instance()  # 获取 ReadFile 实例
    assert_db = read_file.read_config('$.Operations_db.assert_db')  # 使用实例调用 read_config
    db_info = dict(read_file.read_config('$.database.%s' % Acmdopt))  # 使用实例调用 read_config
    if assert_db:  # 判断是否查询数据库断言
        db = DB(db_info)
    else:
        db = None

    yield db

    if assert_db:  # 判断是否查询数据库断言
        db.close()

# 备份恢复数据库
@pytest.fixture(scope="session", autouse=True)
def bac_rec(Acmdopt):
    read_file = get_readfile_instance()  # 获取 ReadFile 实例
    db_config = read_file.read_config('$.database.%s' % Acmdopt)  # 使用实例调用 read_config
    if isinstance(db_config, dict):
        db_data = db_config
    else:
        db_data = {"key": db_config}  # 将非字典数据转换为字典

    BR = BackupRecovery(db_data['data'])
    db_bak_path = './config/ry-vue_bak.sql'  # 当前数据库备份文件
    db_re_path = './config/ry-vue_re.sql'  # 初始化好测试数据的数据库 sql 文件
    backup = read_file.read_config('$.Operations_db.backup')  # 使用实例调用 read_config
    if backup:
        BR.backup(db_bak_path)
        BR.recovery(db_re_path)
    yield
    recovery = read_file.read_config('$.Operations_db.recovery')  # 使用实例调用 read_config
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
        _SUCCESS_RATE = round(_RATE, 2)
    except ZeroDivisionError:
        _SUCCESS_RATE = 0.00  # 将字符串改为浮点数

    Logger.info(f"用例成功率:{_SUCCESS_RATE}")
    result_data_test = {
        "_TOTAL": f"{_TOTAL}",
        '_PASSED': f"{_PASSED}",
        "_ERROR": f" {_ERROR}",
        "_FAILED": f" {_FAILED}",
        "_SKIPPED": f" {_SKIPPED}",
        "_TIMES": f"{round(_TIMES, 2)} s",
        "_SUCCESS_RATE": f"{_SUCCESS_RATE}",
    }
    ExchangeData.post_pytest_summary(result_data_test)  # 测试结果添加到变量池
    with open("result.txt", "w") as fp:  # 测试结果保存到本地 result.txt
        fp.write("_TOTAL=%s" % _TOTAL + "\n")
        fp.write("_PASSED=%s" % _PASSED + "\n")
        fp.write("_FAILED=%s" % _FAILED + "\n")
        fp.write("_ERROR=%s" % _ERROR + "\n")
        fp.write("_SKIPPED=%s" % _SKIPPED + "\n")
        fp.write("_SUCCESS_RATE=%.2f%%" % _SUCCESS_RATE + "\n")  # 这里不会再报错
        fp.write("_TIMES=%.2fs" % _TIMES)