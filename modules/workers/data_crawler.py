from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from time import sleep
import os
from selenium.webdriver.chrome.options import Options
from repositories.checkout_events import CheckoutEventRepo
from repositories.employee import EmployeeRepo
import pandas as pd
from modules.workers.base_worker import BaseWorker
from utils.consts import CRAWLER_JOB_TYPE
from models.checking_event import CheckingEvent
from models.employee import Employee
from datetime import datetime, timedelta, time
from repositories.abnormal_checking import AbnormalCheckingRepo
from repositories.job import SettingRepo
from models.abnormal_checking import AbnormalChecking
from dataclasses import dataclass
from dto.settings import SettingType, SettingValue
from functools import lru_cache

# Please not that at the time of developing this system (May/2025), the allowed rest times for each department are specified in the picture "image.png" in folder data
# I am not responsible for later changes to the official timing schedules of those.

driver_options = Options()
driver_options.add_argument("--headless=new")
driver_options.add_argument("--window-size=1200,768")

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
ALLOWED_GAP_MINS = 10
TWELVE_HOURS_MINS = 60 * 12
ALLOWED_BREAK_MINS = 60 # meal + rest time

ASM = "ASM"
PD1 = "PD1"
PD2 = "PD2"
PD3 = "PD3"
TE = "TE"
ME = "ME"
QMD = "QMD"
SMT = "SMT"
GA = "GA"
IE = "IE"
SASM = "SASM"
SWH = "SWH"
EQ = "EQ"
FAEE = "FAEE"
WH = "WH"
IT = "IT"
SCM = "SCM"
OPM = "OPM"
HR = "HR"
EHS = "EHS"
PT = "PT"
PE = "PE"
FD = "FD"
ALL = "ALL"
    

def get_short_department(full_department: str) -> str:
    if len(full_department.strip()) == 0:
        return "UNKNOWN"
    
    split = full_department.split(">")
    if len(split) == 1:
        return split[0].upper()
    elif len(split) > 1:
        return f"{split[-2]}, {split[-1]}".upper()


def calculate_department(full_department: str):
    dept = get_short_department(full_department).upper()

    if "ASM" in dept:
        return ASM
    if "Production Department 1".upper() in dept:
        return PD1
    if "Production Department 2".upper() in dept:
        return PD2
    if "Production Department 3".upper() in dept:
        return PD3
    if "Test Engineering section".upper() in dept:
        return TE
    if "back end".upper() in dept or "back end me".upper() in dept:
        return ME
    if "QMD" in dept:
        return QMD
    if "SMT"in dept:
        return SMT
    if "GA" in dept:
        return GA
    if "Industrial Engineering".upper() in dept:
        return IE
    if "SASM" in dept:
        return SASM
    if PE in dept:
        return PE
    return None
    
def subtract_times(t1: time, t2: time):
    """total mins for t1-t2"""
    today = datetime.today()
    dt1 = datetime.combine(today, t1)
    dt2 = datetime.combine(today, t2)
    return (dt1 - dt2).total_seconds() / 60


def get_hour_min_from_datetime(dt: datetime) -> time:
    return time(dt.hour, dt.minute)


def calculate_time_gap_in_mins(start_time: datetime, end_time: datetime):
    return (end_time - start_time).total_seconds() / 60

@dataclass
class Break(object):
    start_time: time
    end_time: time
    depts: list[str]

    @lru_cache
    @property
    def allowed_mins(self):
        return subtract_times(self.end_time, self.start_time)

    def check_abnormal(self, actual_time_taken_in_mins: float, full_department: str) -> bool:
        """if return true => abnormal"""

        if actual_time_taken_in_mins > self.allowed_mins:
            return True

        dept = calculate_department(full_department)
        if not dept:
            return True
        
        return dept not in self.depts


Eleven_Twelve = Break(time(11, 0), time(12, 0), [PD1, SMT, ASM, TE, PD2, QMD])
ElevenTwenty_TwelveTwenty = Break(time(11, 20), time(12, 20), [PD2, SWH, SASM, EQ, TE, FAEE, ME, WH])
ElevenFourty_TwelveFourty = Break(time(11, 40), time(12, 40), [PD2, SWH, SASM, SCM, HR, GA, EHS, IE, IT, PE, FD])
Twelve_TwelveFourtyFive = Break(time(12, 0), time(12, 45), [PD1, PD2, ASM, SMT])
Sixteen_Seventeen = Break(time(16, 0), time(17, 0), [ALL])
Seventeen_Eighteen = Break(time(17, 0), time(18, 0), [ALL])
TwentyThree_TwentyFour = Break(time(23, 0), time(23, 59, 59), [ALL])
Four_Five = Break(time(4, 0), time(5, 0), [ALL])
Five_Six = Break(time(5, 0), time(6, 0), [ALL])


def classify_break_type(checkout_time: datetime) -> Break | None:
    out_time = get_hour_min_from_datetime(checkout_time)
    if out_time >= Four_Five.start_time:
        return Four_Five
    if out_time >= Five_Six.start_time:
        return Five_Six
    if out_time >= Eleven_Twelve.start_time:
        return Eleven_Twelve
    if out_time >= ElevenTwenty_TwelveTwenty.start_time:
        return ElevenTwenty_TwelveTwenty
    if out_time >= ElevenFourty_TwelveFourty.start_time:
        return ElevenFourty_TwelveFourty
    if out_time >= Twelve_TwelveFourtyFive.start_time:
        return Twelve_TwelveFourtyFive
    if out_time >= Sixteen_Seventeen.start_time:
        return Sixteen_Seventeen
    if out_time >= Seventeen_Eighteen.start_time:
        return Seventeen_Eighteen
    if out_time >= TwentyThree_TwentyFour.start_time:
        return TwentyThree_TwentyFour
    return None


def calculate_abnormal_result(checkout_time: datetime, checkin_time: datetime, department: str):
    """If returns True => Abnormal, False otherwise"""
    actual_gap_mins = calculate_time_gap_in_mins(checkout_time, checkin_time)
    if actual_gap_mins < ALLOWED_GAP_MINS or actual_gap_mins >= TWELVE_HOURS_MINS:
        return False

    if actual_gap_mins > ALLOWED_GAP_MINS:
        break_type = classify_break_type(checkin_time)
        if break_type is None:
            return True
        
    
@dataclass
class CheckOutInfo:
    station: str
    check_time: datetime


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
        self.abnormalRepo = AbnormalCheckingRepo(self.db)
        self.settingRepo = SettingRepo(self.db)

    def stop(self):
        if self.driver:
            self.driver.quit()

    def __crawl_data(self):
        try:
            self.driver = webdriver.Chrome(options=driver_options)
            self.driver.get(self.URL)
            self.driver.implicitly_wait(10)

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
            sleep(3)

            #enter identity access search
            self.findElement('./html/body/div[6]/div[1]/div[1]/div[1]/input',['input'],'identity access search')
            #wait for result
            sleep(1)
            #click on identity access search
            self.findElement('./html/body/div[6]/div[1]/div[1]/div[2]/div/div[1]')
            #wait for new page load
            sleep(2)

            #choose floor need to double click
            self.doubleclickElement('./html/body/div[5]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div[1]/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div[3]/ul/div/div/div/ul/li[1]/div/span[2]')
            #choose status type
            self.findElement('./html/body/div[5]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div[1]/div[1]/div[2]/div/div/div[3]/div[2]/div/input')
            # sleep(1)
            self.findElement('./html/body/div[8]/div/div[1]/ul/li[2]/span')

            #click search button
            self.findElement('./html/body/div[5]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div[1]/div[1]/div[3]/button')
            #click export button
            self.findElement('./html/body/div[5]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div[2]/div[1]/button')
            #click csv radio button
            sleep(1)
            self.findElement('.//*[@id="accessControl"]/div/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div[2]/div[1]/label')

            #click save button
            self.findElement('./html/body/div[5]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div[3]/button')

            # get file name
            sleep(4)
            first_elem = self.driver.find_element(By.XPATH, './/*[@id="body"]/div[9]/div[1]/div/div[1]/p[1]')
            file_name = first_elem.text

            self.driver.quit()

            return file_name, None
        except Exception as e:
            self.stop()
            return None, e

    def __try_insert_employee(self, item: dict):
        try:
            # is_visitor = False
            visition = item.get(PERSON_VISITOR, "")
            is_visitor = not visition or "person" not in f"{visition}".lower()

            department = get_short_department(item.get(DEPARTMENT))

            new_employee = Employee(
                id = item.get(PERSON_NO),
                first_name = item.get(FIRST_NAME, ""),
                last_name = item.get(LAST_NAME),
                card_no = "",
                is_visitor = is_visitor,
                department = department,
            )
            self.employeeRepo.create(new_employee)
        except Exception:
            # already exist, dont raise
            return
        
    def __handle_delete_file(self, file_name: str):
        dir_path = os.path.join(DATA_FOLDER_PATH, file_name)
        full_file_path = os.path.join(dir_path, file_name + ".xlsx")

        if os.path.exists(full_file_path):
            os.remove(full_file_path)
            os.rmdir(dir_path)

    def handle_data(self, file_name: str):
        # wait for file to ready:
        full_file_path = os.path.join(DATA_FOLDER_PATH, file_name, file_name + ".xlsx")
        tries = 1
        file_exist = os.path.exists(full_file_path)
        total_tries = 3

        while not file_exist and tries <= total_tries:
            sleep(tries * 2)
            file_exist = os.path.exists(full_file_path)
            tries += 1

        if not file_exist:
            return FileNotFoundError(f"the file path {full_file_path} does not exist.")

        try:
            # skip first 7 rows since those data is not needed
            dframe = pd.read_excel(full_file_path, sheet_name=self.SHEET_NAME, skiprows=7, engine='openpyxl')
            latest_success_job = self.jobRepo.get_last_job(only_success=True)

            dframe = dframe.sort_values(by=[TIME], ascending=True)

            meet_map: dict[str, CheckOutInfo] = {}
            checkins_without_checkout_data: list[CheckingEvent] = []

            for _, item in dframe.iterrows():
                # we only process checking records that happend when or after last job success run
                # This helps we avoid doing unnecessasy process
                check_time = item.get(TIME)
                if check_time is None:
                    continue

                check_time = datetime.strptime(check_time.strip(), "%Y-%m-%d %H:%M:%S")
                if latest_success_job and latest_success_job.execution_at > check_time:
                    continue

                employee_id = item.get(PERSON_NO, None)
                if not employee_id:
                    continue

                checking_station = item.get(ACCESS_POINT, "")
                if not checking_station:
                    continue

                checking_station = checking_station.strip().lower()

                is_checkin = "face" in checking_station

                self.__try_insert_employee(item)

                if is_checkin:
                    last_checkout_data = meet_map.get(employee_id, None)
                    if not last_checkout_data:
                        check_evt = CheckingEvent(
                            employee_id=employee_id,
                            is_checkin=True,
                            time=check_time,
                            station=checking_station,
                        )
                        # meaning there is no last checkout data
                        checkins_without_checkout_data.append(check_evt)
                    else:
                        gap_time = check_time - last_checkout_data.check_time
                        gap_mins = gap_time.total_seconds() / 60
                        if gap_mins > ALLOWED_GAP_MINS and gap_mins < TWELVE_HOURS_MINS:
                            # abnormal
                            # insert to database for reporting
                            abnormal_checking_record = AbnormalChecking(
                                employee_id=employee_id,
                                in_time=check_time,
                                out_time=last_checkout_data.check_time,
                                total_mins=gap_mins,
                                checkin_station=checking_station,
                                checkout_station=last_checkout_data.station,
                            )
                            self.abnormalRepo.create(abnormal_checking_record)

                        # remove data from map
                        del meet_map[employee_id]
                else:
                    # check out, insert to meet map
                    meet_map[employee_id] = CheckOutInfo(station=checking_station, check_time=check_time)


            # done parsing file, begin handling missing data

            for event in checkins_without_checkout_data:
                # find last check out for each event
                last_checkout = self.checkingEventRepo.find_last_checking_event_by_employee_id(event.employee_id, check_in=False)
                if last_checkout:
                    gap_time = event.time - last_checkout.time
                    gap_mins = gap_time.total_seconds() / 60
                    if gap_mins > ALLOWED_GAP_MINS and gap_mins < TWELVE_HOURS_MINS:
                        abnormal_checking_record = AbnormalChecking(
                            employee_id=event.employee_id,
                            in_time=event.time,
                            out_time=last_checkout.time,
                            total_mins=gap_mins,
                            checkin_station=checking_station,
                            checkout_station=last_checkout.station,
                        )
                        self.abnormalRepo.create(abnormal_checking_record)
            
            if len(meet_map) > 0:
                # meaning some check outs do not have checkin events yet, just save them to database for later reference
                for (employee_id, checkout_data) in meet_map.items():
                    check_evt = CheckingEvent(
                        employee_id=employee_id,
                        is_checkin=False,
                        time=checkout_data.check_time,
                        station=checkout_data.station,
                    )
                    self.checkingEventRepo.create(check_evt)

        except Exception as e:
            return e

    def execute(self):
        setting = self.settingRepo.get_by_type(SettingType.data_crawler.value)
        if setting and setting.value == SettingValue.disable_data_crawler.value:
            return

        tries = 0
        total_tries = 3

        while tries < total_tries:
            file_name, error = self.__crawl_data()
            if error:
                reason = f"{error}"
                self.set_job_error(CRAWLER_JOB_TYPE, reason)
                tries += 1
                continue

            error = self.handle_data(file_name)
            if error:
                reason = f"{error}"
                self.set_job_error(CRAWLER_JOB_TYPE, reason)
                tries += 1
                continue

            self.set_job_success(CRAWLER_JOB_TYPE)
            self.__handle_delete_file(file_name)
            self.stop()
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
