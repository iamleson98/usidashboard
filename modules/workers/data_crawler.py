from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import os
from selenium.webdriver.chrome.options import Options
from repositories.checkout_events import CheckoutEventRepo
from repositories.employee import EmployeeRepo
import pandas as pd
from modules.workers.base_worker import BaseWorker
from utils.consts import CRAWLER_JOB_TYPE
from models.checking_event import CheckingEvent
from models.employee import Employee
from datetime import datetime
import subprocess


driver_options = Options()
driver_options.add_argument("--headless=new")
driver_options.add_argument("--window-size=1366,768")

# The Hk web requires a client tool to be installed before we can connect and export checking data
# When we export, that tool save to folder "C:\Users\Public\HCWebControlService" on windows

if os.name == 'nt':
    DATA_FOLDER_PATH = r"C:\Users\Public\HCWebControlService"
else:
    DATA_FOLDER_PATH = "unknown"

FIRST_NAME = "First Name"
LAST_NAME = "Last Name"
NAME = "Name"
PERSON_NO = "Person No."
PERSON_VISITOR = "Person/Visitor"
ACCESS_POINT = "Access Point"
TIME = "Time"
DEPARTMENT = "Department"

def change_file_write_permissions(path: str):
    """grant write permission on files on Windows"""
    cmd = f'icacls "{path}" /grant Everyone:(W)'
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        if result.returncode == 0:
            return True
        return False
    except Exception:
        return False

class DataCrawlerWorker(BaseWorker):
    USER_NAME = "PDVIP"
    PASSWORD = "USIVIP@2025"
    URL = "http://10.53.232.80/#/"
    SHEET_NAME = "Sheet1"

    def __init__(
        self, 
    ):
        super().__init__()
        self.checkingEventRepo = CheckoutEventRepo(self.db)
        self.employeeRepo = EmployeeRepo(self.db)

    def stop(self):
        if self.driver:
            self.driver.quit()

    def __crawl_data(self):
        try:
            self.driver = webdriver.Chrome(options=driver_options)
            self.driver.get(self.URL)
            self.driver.implicitly_wait(4)

            #username input
            self.findElement('./html/body/div[5]/div/div/div/div[2]/div[3]/form/div[3]/div/div/span[1]/input',['input'],self.USER_NAME)
            #password input
            self.findElement('./html/body/div[5]/div/div/div/div[2]/div[3]/form/div[4]/div/div[1]/input',['input'],self.PASSWORD)
            #press login button
            self.findElement('./html/body/div[5]/div/div/div/div[2]/div[3]/form/div[5]/div/button')

            #click access tab
            self.findElement('./html/body/div[5]/div/div/div/div[1]/div[2]/div[2]/div/div[3]/div[1]/div/div/div/div[1]')
            #click search button
            self.findElement('./html/body/div[5]/div/div/div/div[1]/div[2]/div[3]/div[4]')
            #wait for input to appear
            time.sleep(3)

            #enter identity access search
            self.findElement('./html/body/div[6]/div[1]/div[1]/div[1]/input',['input'],'identity access search')
            #wait for result
            time.sleep(1)
            #click on identity access search
            self.findElement('./html/body/div[6]/div[1]/div[1]/div[2]/div/div[1]')
            #wait for new page load
            time.sleep(2)

            #choose floor need to double click
            self.doubleclickElement('./html/body/div[5]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div[1]/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div[3]/ul/div/div/div/ul/li[1]/div/span[2]')
            #choose status type
            self.findElement('./html/body/div[5]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div[1]/div[1]/div[2]/div/div/div[3]/div[2]/div/input')
            # time.sleep(1)
            self.findElement('./html/body/div[8]/div/div[1]/ul/li[2]/span')

            #click search button
            self.findElement('./html/body/div[5]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div[1]/div[1]/div[3]/button')
            #click export button
            self.findElement('./html/body/div[5]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div[2]/div[1]/button')
            #click csv radio button
            time.sleep(1)
            self.findElement('.//*[@id="accessControl"]/div/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div[2]/div[1]/label')

            #click save button
            self.findElement('./html/body/div[5]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div[3]/button')

            # get file name
            time.sleep(4)
            first_elem = self.driver.find_element(By.XPATH, './/*[@id="body"]/div[9]/div[1]/div/div[1]/p[1]')
            file_name = first_elem.text

            self.driver.quit()

            return file_name, None
        except Exception as e:
            return None, e

    def __try_insert_employee(self, item: dict):
        try:
            # is_visitor = False
            visition = item.get(PERSON_VISITOR, "")
            is_visitor = not visition or "person" not in f"{visition}".lower()

            new_employee = Employee(
                id = item.get(PERSON_NO),
                first_name = item.get(FIRST_NAME, ""),
                last_name = item.get(LAST_NAME),
                card_no = "",
                is_visitor = is_visitor,
                department = item.get(DEPARTMENT),
            )
            self.employeeRepo.create(new_employee)
        except Exception:
            # already exist, dont raise
            return

    def __handle_data(self, file_name: str):
        time.sleep(5) # wait for the file to get ready

        full_file_path = os.path.join(DATA_FOLDER_PATH, file_name, file_name + ".xlsx")
        try:
            # skip first 7 rows since those data is not needed
            dframe = pd.read_excel(full_file_path, sheet_name=self.SHEET_NAME, skiprows=7, engine='openpyxl')
            latest_job = self.jobRepo.get_last_job(only_success=True)

            for _, item in dframe.iterrows():
                # we only process checking records that happend when or after last job success run
                # This helps we avoid doing unnecessasy process
                check_time = item.get(TIME)
                if check_time is None:
                    continue

                check_time = datetime.strptime(check_time, "%Y-%m-%d %H:%M:%S")
                if latest_job and latest_job.execution_at > check_time:
                    continue

                employee_id = item.get(PERSON_NO, None)
                if not employee_id:
                    continue

                checking_type = item.get(ACCESS_POINT, "")
                if not checking_type:
                    continue

                checking_type = f"{checking_type}".lower()
                type_ = 1
                if "face" not in checking_type: # means check out
                    type_ = 0

                check_evt = CheckingEvent(
                    employee_id=employee_id,
                    type=type_,
                    time=check_time,
                )

                self.__try_insert_employee(item)

                self.checkingEventRepo.create(check_evt)
        except Exception as e:
            return e

    def execute(self):
        file_name, error = self.__crawl_data()
        if error:
            reason = f"{error}"
            self.set_job_error(CRAWLER_JOB_TYPE, reason)
            return

        error = self.__handle_data(file_name)
        if error:
            reason = f"{error}"
            self.set_job_error(CRAWLER_JOB_TYPE, reason)
            return
        
        self.set_job_success(CRAWLER_JOB_TYPE)
        return

    def findElement(self, Xpath, actions=[], var=''):
        element_box = self.driver.find_element(By.XPATH, Xpath)
        element_box.click()
        if ("input" in actions):
            element_box.send_keys(var)

    def doubleclickElement(self, Xpath):
        element_click = self.driver.find_element(By.XPATH, Xpath)
        ActionChains(self.driver) \
            .double_click(element_click) \
            .perform()

CRAWLER_WORKER = DataCrawlerWorker()
