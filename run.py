import logging
import subprocess

import pytest
import os

'''def run(task_id):
    report_dir = f'./target/allure-results_{task_id}'
    os.makedirs(report_dir, exist_ok=True)
    logging.debug(f"Current Task ID: {task_id}")
    logging.basicConfig(level=logging.DEBUG)
    pytest.main(['./test_caes', '-vs', "--env=test", "--alluredir", report_dir])
    logging.debug("开始调用run了") '''

def run(task_id):
    # Define the directory for Allure results and report
    report_dir = f'./target/allure-results_{task_id}'
    report_output_dir = f'./target/allure-report_{task_id}'
    
    # Create directories if they don't exist
    os.makedirs(report_dir, exist_ok=True)
    os.makedirs(report_output_dir, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(f"Current Task ID: {task_id}")
    
    # Run pytest with Allure results
    pytest.main(['./test_caes', '-vs', "--env=test", "--alluredir", report_dir])
    
    # Generate Allure report
    #allure_command = ['allure', 'generate', report_dir, '-o', report_output_dir, '--clean']
    #subprocess.run(allure_command, check=True)
    
    # Serve Allure report online
    #serve_command = ['allure', 'serve', report_dir]
    #subprocess.run(serve_command, check=True)
    
    logging.debug("Allure report generated and served online.")