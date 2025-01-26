import logging
import pytest
import os

def run(task_id):
    report_dir = f'./target/allure-results_{task_id}'
    os.makedirs(report_dir, exist_ok=True)
    logging.debug(f"Current Task ID: {task_id}")
    logging.basicConfig(level=logging.DEBUG)
    pytest.main(['./test_caes', '-vs', "--env=test"])
    logging.debug("开始调用run了")