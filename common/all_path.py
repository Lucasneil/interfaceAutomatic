
import os

base_path = os.path.dirname(os.path.dirname(__file__))

appPath = os.path.join(base_path, 'app')
dataPath = os.path.join(base_path, 'data')
configPath = os.path.join(base_path, 'config')
logPath = os.path.join(base_path,  'logs')
picturePath = os.path.join(base_path, 'png')
reportsPath = os.path.join(base_path, 'target', 'allure-report')
screenPath = os.path.join(base_path,  'screencap')
targetPath=os.path.join(base_path, 'target')
#Start_server_bat=os.path.join(base_path, 'config',"Start_server.bat")
Start_server_bat=os.path.join(base_path, 'config',"fileServices.exe")
images_Path=os.path.join(base_path, 'config',"png") #./config/png
environmentPath=os.path.join(base_path,  'config',"environment.properties")
allure_results = os.path.join(targetPath, 'allure-results','environment.properties')

