import logging
import pytest
import os

def run(task_id):
    report_dir = './report'
    #report_dir = f'./target/allure-results_{task_id}'
    #os.makedirs(report_dir, exist_ok=True)
    logging.debug(f"Current Task ID: {task_id}")
    logging.basicConfig(level=logging.DEBUG)
    os.makedirs(report_dir, exist_ok=True)  # Ensure the report directory exists
    report_file = f'{report_dir}/report_{task_id}.html'
    #pytest.main(['./test_caes', '-vs', "--env=test",f'--html={report_file}',"--self-contained-html"])
    pytest.main(['./test_caes', '-vs', "--env=test", f'--html={report_file}', "--self-contained-html"])
    logging.debug("开始调用run了")