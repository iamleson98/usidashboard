from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from time import sleep
import os
from selenium.webdriver.chrome.options import Options
from repositories.checkout_events import CheckingEventRepo
from repositories.aggregation import AggregationRepo
from repositories.employee import EmployeeRepo
from models.aggregations import Aggregation, DATE_FORMAT
import pandas as pd
from modules.workers.base_worker import BaseWorker
from utils.consts import CRAWLER_JOB_TYPE
from models.checking_event import CheckingEvent
from models.employee import Employee
from datetime import datetime, time
from repositories.abnormal_checking import AbnormalCheckingRepo
from repositories.job import SettingRepo
from models.abnormal_checking import AbnormalChecking
from dataclasses import dataclass
from dto.settings import SettingType, SettingValue
from dto.employee import ShortDepartment
from dto.aggregation import AttendaceRecord
from models.aggregations import DATE_FORMAT

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
# ALLOWED_BREAK_MINS = 60 # meal + rest time


def get_short_department(full_department: str) -> str:
    if len(full_department.strip()) == 0:
        return ShortDepartment.UNKNOWN.value
    
    split = full_department.split(">")
    if len(split) == 1:
        return split[0]
    elif len(split) > 1:
        return f"{split[-2]}, {split[-1]}"


def calculate_department(full_department: str):
    dept = get_short_department(full_department).upper()

    if "QMD" in dept or "MQA" in dept:
        return ShortDepartment.QMD
    if "Equipment Engineering".upper() in dept or "EQ" in dept:
        return ShortDepartment.EQ
    if "SASM" in dept:
        return ShortDepartment.SASM
    if "ASM" in dept:
        return ShortDepartment.ASM
    if "Production Department 1".upper() in dept:
        return ShortDepartment.PD1
    if "Production Department 2".upper() in dept:
        return ShortDepartment.PD2
    if "Test Department".upper() in dept:
        return ShortDepartment.TE
    if "Production Department 3".upper() in dept:
        return ShortDepartment.PD3
    if "Test Engineering section".upper() in dept:
        return ShortDepartment.TE
    if "back end".upper() in dept or "back end me".upper() in dept:
        return ShortDepartment.ME
    if "front end".upper() in dept or "front end me".upper() in dept:
        return ShortDepartment.ME
    if "Supporter".upper() in dept:
        return ShortDepartment.UNKNOWN
    if "ME" in dept:
        return ShortDepartment.ME
    if "System Assembly Manufacturing Engineer".upper() in dept or "SME" in dept:
        return ShortDepartment.SME
    if "TE" in dept:
        return ShortDepartment.TE
    if "PT" in dept:
        return ShortDepartment.PT
    if ShortDepartment.SMT.value in dept:
        return ShortDepartment.SMT
    if ShortDepartment.FA.value in dept or "Factory Affair".upper() in dept:
        return ShortDepartment.FA
    if "GA" in dept:
        return ShortDepartment.GA
    if "Industrial Engineering".upper() in dept or "IE" in dept:
        return ShortDepartment.IE
    if "PE" in dept:
        return ShortDepartment.PE
    if "Warehouse Section".upper() in dept:
        return ShortDepartment.WH
    if "Test Sub-Section 1".upper() in dept:
        return ShortDepartment.PD1
    if "Test Sub-Section 2".upper() in dept:
        return ShortDepartment.PD2
    if "Test Sub-Section 3".upper() in dept:
        return ShortDepartment.PD3
    return ShortDepartment.UNKNOWN
    
def subtract_times(t1: time, t2: time):
    """total mins for t1-t2"""
    today = datetime.today()
    dt1 = datetime.combine(today, t1)
    dt2 = datetime.combine(today, t2)
    return (dt1 - dt2).total_seconds() / 60


def calculate_time_gap_in_mins(start_time: datetime, end_time: datetime):
    return (end_time - start_time).total_seconds() / 60

class Break(object):
    def __init__(self, start_time, end_time, depts):
        self.start_time = start_time
        self.end_time = end_time
        self.depts = depts
        self.allowed_mins = subtract_times(end_time, start_time)

    def check_abnormal(self, actual_time_taken_in_mins: float, full_department: str) -> bool:
        """if return true => abnormal"""

        if actual_time_taken_in_mins > self.allowed_mins:
            return True
        
        if ShortDepartment.ALL in self.depts:
            return actual_time_taken_in_mins > self.allowed_mins

        dept = calculate_department(full_department)
        if not dept:
            return True

        if dept not in self.depts:
            return actual_time_taken_in_mins > ALLOWED_GAP_MINS

        return actual_time_taken_in_mins > self.allowed_mins
    

def handle_parse_time_from_data_file_name(file_name: str):
    """Identity Access Search_2025_06_09_15_21_36_762"""
    split_name = file_name.split("_")
    numbers = filter(lambda item: item.isdigit(), split_name)
    numbers = list(numbers)
    if len(numbers) != 7:
        return None
    
    return datetime.strptime(f"{numbers[0]}-{numbers[1]}-{numbers[2]} {numbers[3]}:{numbers[4]}:{numbers[5]}", DATE_FORMAT)
    

Eleven_Twelve = Break(time(11, 0), time(12, 0), [ShortDepartment.PD1, ShortDepartment.SMT, ShortDepartment.ASM, ShortDepartment.TE, ShortDepartment.PD2, ShortDepartment.QMD])
ElevenTwenty_TwelveTwenty = Break(time(11, 20), time(12, 20), [ShortDepartment.PD2, ShortDepartment.SWH, ShortDepartment.SASM, ShortDepartment.EQ, ShortDepartment.TE, ShortDepartment.FAEE, ShortDepartment.ME, ShortDepartment.WH, ShortDepartment.SME])
ElevenFourty_TwelveFourty = Break(time(11, 40), time(12, 40), [ShortDepartment.PD2, ShortDepartment.SWH, ShortDepartment.SASM, ShortDepartment.SCM, ShortDepartment.HR, ShortDepartment.GA, ShortDepartment.EHS, ShortDepartment.IE, ShortDepartment.IT, ShortDepartment.PE, ShortDepartment.FD, ShortDepartment.FA])
Twelve_TwelveFourtyFive = Break(time(12, 0), time(12, 45), [ShortDepartment.PD1, ShortDepartment.PD2, ShortDepartment.ASM, ShortDepartment.SMT])
Sixteen_Seventeen = Break(time(16, 0), time(17, 0), [ShortDepartment.ALL])
Seventeen_Eighteen = Break(time(17, 0), time(18, 0), [ShortDepartment.ALL])
TwentyThree_TwentyFour = Break(time(23, 0), time(23, 59, 59), [ShortDepartment.ALL])
Four_Five = Break(time(4, 0), time(5, 0), [ShortDepartment.ALL])
Five_Six = Break(time(5, 0), time(6, 0), [ShortDepartment.ALL])
Zero_One = Break(time(0, 0), time(1, 0), [ShortDepartment.ALL])


def classify_break_type(checkout_time: datetime) -> Break | None:
    out_time = time(checkout_time.hour, checkout_time.minute)

    if out_time >= TwentyThree_TwentyFour.start_time and out_time < TwentyThree_TwentyFour.end_time:
        return TwentyThree_TwentyFour
    if out_time >= Seventeen_Eighteen.start_time and out_time < Seventeen_Eighteen.end_time:
        return Seventeen_Eighteen
    if out_time >= Sixteen_Seventeen.start_time and out_time < Sixteen_Seventeen.end_time:
        return Sixteen_Seventeen
    if out_time >= Twelve_TwelveFourtyFive.start_time and out_time < Twelve_TwelveFourtyFive.end_time:
        return Twelve_TwelveFourtyFive
    if out_time >= ElevenFourty_TwelveFourty.start_time and out_time < ElevenFourty_TwelveFourty.end_time:
        return ElevenFourty_TwelveFourty
    if out_time >= ElevenTwenty_TwelveTwenty.start_time and out_time < ElevenTwenty_TwelveTwenty.end_time:
        return ElevenTwenty_TwelveTwenty
    if out_time >= Eleven_Twelve.start_time and out_time < Eleven_Twelve.end_time:
        return Eleven_Twelve
    if out_time >= Five_Six.start_time and out_time < Five_Six.end_time:
        return Five_Six
    if out_time >= Four_Five.start_time and out_time < Four_Five.end_time:
        return Four_Five
    if out_time >= Zero_One.start_time and out_time < Zero_One.end_time:
        return Zero_One
    return None


def calculate_abnormal_result(checkout_time: datetime, checkin_time: datetime, department: str):
    """If returns True => Abnormal, False otherwise"""
    actual_gap_mins = calculate_time_gap_in_mins(checkout_time, checkin_time)
    # if total time out > 10 and < 11, still valid
    if actual_gap_mins < ALLOWED_GAP_MINS or actual_gap_mins >= TWELVE_HOURS_MINS:
        return actual_gap_mins, False

    break_type = classify_break_type(checkout_time)
    if break_type is None:
        return actual_gap_mins, actual_gap_mins > ALLOWED_GAP_MINS
    return actual_gap_mins, break_type.check_abnormal(actual_gap_mins, department)


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
        self.checkingEventRepo = CheckingEventRepo(self.db)
        self.employeeRepo = EmployeeRepo(self.db)
        self.abnormalRepo = AbnormalCheckingRepo(self.db)
        self.settingRepo = SettingRepo(self.db)
        self.aggregateRepo = AggregationRepo(self.db)

    def stop(self):
        if self.driver:
            self.driver.quit()

    def __crawl_data(self):
        def find_element(Xpath, actions=[], var=''):
            element_box = self.driver.find_element(By.XPATH, Xpath)
            element_box.click()
            if ("input" in actions):
                element_box.send_keys(var)

        def double_click_element(Xpath):
            element_click = self.driver.find_element(By.XPATH, Xpath)
            ActionChains(self.driver).double_click(element_click).perform()
        
        try:
            self.driver = webdriver.Chrome(options=driver_options)
            self.driver.get(self.URL)
            self.driver.implicitly_wait(10)

            #username input
            find_element('./html/body/div[5]/div/div/div/div[2]/div[3]/form/div[3]/div/div/span[1]/input',['input'],self.USER_NAME)
            #password input
            find_element('./html/body/div[5]/div/div/div/div[2]/div[3]/form/div[4]/div/div[1]/input',['input'],self.PASSWORD)
            #press login button
            find_element('./html/body/div[5]/div/div/div/div[2]/div[3]/form/div[5]/div/button')

            #click access tab
            find_element('./html/body/div[5]/div/div/div/div[1]/div[2]/div[2]/div/div[3]/div[1]/div/div/div/div[1]')
            #click search button
            find_element('./html/body/div[5]/div/div/div/div[1]/div[2]/div[3]/div[4]')
            #wait for input to appear
            sleep(3)

            #enter identity access search
            find_element('./html/body/div[6]/div[1]/div[1]/div[1]/input',['input'],'identity access search')
            #wait for result
            sleep(1)
            #click on identity access search
            find_element('./html/body/div[6]/div[1]/div[1]/div[2]/div/div[1]')
            #wait for new page load
            sleep(2)

            #choose floor need to double click
            double_click_element('./html/body/div[5]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div[1]/div[1]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/div[3]/ul/div/div/div/ul/li[1]/div/span[2]')
            #choose status type
            find_element('./html/body/div[5]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div[1]/div[1]/div[2]/div/div/div[3]/div[2]/div/input')
            # sleep(1)
            find_element('./html/body/div[8]/div/div[1]/ul/li[2]/span')

            #click search button
            find_element('./html/body/div[5]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div[1]/div[1]/div[3]/button')
            #click export button
            find_element('./html/body/div[5]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div[4]/div[2]/div[1]/button')
            #click csv radio button
            sleep(1)
            find_element('.//*[@id="accessControl"]/div/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div[2]/div[1]/label')

            #click save button
            find_element('./html/body/div[5]/div/div/div/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div[5]/div[2]/div[2]/div/div[3]/button')

            # get file name
            sleep(4)
            first_elem = self.driver.find_element(By.XPATH, './/*[@id="body"]/div[9]/div[1]/div/div[1]/p[1]')
            file_name = first_elem.text

            self.driver.quit()

            return file_name, None
        except Exception as e:
            self.driver.quit()
            return None, e

    def __try_insert_employee(self, item: dict):
        try:
            # is_visitor = False
            visition = item.get(PERSON_VISITOR, "")
            is_visitor = not visition or "person" not in f"{visition}".lower()

            full_dept = item.get(DEPARTMENT)
            department = get_short_department(full_dept)
            short_dept = calculate_department(full_dept).value

            new_employee = Employee(
                id = item.get(PERSON_NO),
                first_name = item.get(FIRST_NAME, ""),
                last_name = item.get(LAST_NAME),
                card_no = "",
                is_visitor = is_visitor,
                department = department,
                short_dept = short_dept,
            )
            self.employeeRepo.create(new_employee)
        except Exception:
            # already exist, dont raise
            return
        
    def handle_delete_file(self, file_name: str):
        dir_path = os.path.join(DATA_FOLDER_PATH, file_name)
        full_file_path = os.path.join(dir_path, file_name + ".xlsx")

        if os.path.exists(full_file_path):
            os.remove(full_file_path)
            os.rmdir(dir_path)

    def handle_data(self, file_name: str):
        # STEP 1) READ FILE
        full_file_path = os.path.join(DATA_FOLDER_PATH, file_name, file_name + ".xlsx")
        file_exist = os.path.exists(full_file_path)

        if not file_exist:
            return FileNotFoundError(f"handle_data: the file path {full_file_path} does not exist.")

        try:
            # skip first 7 rows since those data is not needed
            dframe = pd.read_excel(full_file_path, sheet_name=self.SHEET_NAME, skiprows=7, engine='openpyxl')
            latest_success_job = self.jobRepo.get_last_job(only_success=True)

            dframe = dframe.sort_values(by=[TIME], ascending=True)
            meet_map: dict[str, CheckOutInfo] = {}
            checkins_without_checkout_data: list[tuple[CheckingEvent, str]] = []

            for _, item in dframe.iterrows():
                # we only process checking records that happend when or after last job success run
                # This helps we avoid doing unnecessasy process
                check_time = item.get(TIME)
                if check_time is None:
                    continue

                check_time = datetime.strptime(check_time.strip(), "%Y-%m-%d %H:%M:%S")
                if latest_success_job and latest_success_job.execution_at > check_time:
                    # skip items that are already processed
                    continue

                employee_id = item.get(PERSON_NO, None)
                if not employee_id:
                    continue

                checking_station = item.get(ACCESS_POINT, "")
                if not checking_station:
                    continue

                department = item.get(DEPARTMENT)

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
                        checkins_without_checkout_data.append((check_evt, department, ))
                    else:
                        gap_mins, is_abnormal = calculate_abnormal_result(last_checkout_data.check_time, check_time, department)
                        if is_abnormal:
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

            # STEP 3) done parsing file, begin handling checkins without checkout data
            for (event, department) in checkins_without_checkout_data:
                # find last check out for each event
                last_checkout = self.checkingEventRepo.find_last_checking_event_by_employee_id(event.employee_id, check_in=False)
                if last_checkout:
                    gap_mins, is_abnormal = calculate_abnormal_result(last_checkout.time, event.time, department)
                    if is_abnormal:
                        abnormal_checking_record = AbnormalChecking(
                            employee_id=event.employee_id,
                            in_time=event.time,
                            out_time=last_checkout.time,
                            total_mins=gap_mins,
                            checkin_station=checking_station,
                            checkout_station=last_checkout.station,
                        )
                        self.abnormalRepo.create(abnormal_checking_record)

                    self.checkingEventRepo.delete(last_checkout)
            
            # STEP 4) If there are some checkouts wihout checking data yet, save them to db for later reference
            if len(meet_map) > 0:
                for (employee_id, checkout_data) in meet_map.items():
                    check_evt = CheckingEvent(
                        employee_id=employee_id,
                        is_checkin=False,
                        time=checkout_data.check_time,
                        station=checkout_data.station,
                    )
                    self.checkingEventRepo.create(check_evt)

            return None

        except Exception as e:
            return e
        
    def handle_aggregate(self, file_name: str):
        full_file_path = os.path.join(DATA_FOLDER_PATH, file_name, file_name + ".xlsx")
        file_exist = os.path.exists(full_file_path)

        if not file_exist:
            return FileNotFoundError(f"handle_aggregate: the file path {full_file_path} does not exist.")
        
        # the time must be the time this file is exported, this ensure the integrity of result data
        crawl_time: datetime = handle_parse_time_from_data_file_name(file_name)

        # STEP 1) FETCH EXISTING AGGREGATION RECORD FROM DB
        aggregation = self.aggregateRepo.get_one()
        if aggregation is None:
            return Exception("could not find aggregation record")

        normalized_aggrs = aggregation.normalize()

        try:
            # skip first 7 rows since those data is not needed
            dframe = pd.read_excel(full_file_path, sheet_name=self.SHEET_NAME, skiprows=7, engine='openpyxl')

            FLOOR_NUMBERS = ['1', '2', '3', '4']

            # STEP 5) SAVE new aggregation data, we only keep the latest 10 items
            new_aggregation = AttendaceRecord(
                time=crawl_time.strftime(DATE_FORMAT),
                live_count={},
            )

            for floor_no in FLOOR_NUMBERS:
                checkins = dframe.loc[(dframe[ACCESS_POINT].str.startswith(floor_no)) & (dframe[ACCESS_POINT].str.lower().str.find("face") >= 0)].shape[0]
                checkouts = dframe.loc[(dframe[ACCESS_POINT].str.startswith(floor_no)) & (dframe[ACCESS_POINT].str.lower().str.find("face") == -1)].shape[0]

                new_aggregation.live_count[f"floor {floor_no}"] = checkins - checkouts
            
            normalized_aggrs.live_attendances.append(new_aggregation)
            normalized_aggrs.updated_at = crawl_time

            while len(normalized_aggrs.live_attendances) > 10:
                normalized_aggrs.live_attendances.pop(0)

            self.aggregateRepo.update(normalized_aggrs.id, Aggregation.from_schema(normalized_aggrs))

            return None

        except Exception as e:
            return e

    def execute(self):
        execution_time = datetime.now()

        # check if setting alow run
        setting = self.settingRepo.get_by_type(SettingType.data_crawler.value)
        if setting and setting.value == SettingValue.disable_data_crawler.value:
            return

        # crawl data job
        crawl_tries = 0
        total_tries = 3
        file_name = None
        crawl_error = None

        while crawl_tries < total_tries and not file_name:
            file_name, crawl_error = self.__crawl_data()
            if crawl_error:
                crawl_tries += 1
                continue
            break

        if crawl_error:
            self.set_job_error(CRAWLER_JOB_TYPE, f"{crawl_error}", execution_at=execution_time)
            return
        
        # handlecheck abnormals job
        data_handle_tries = 0
        data_handle_error = None

        while data_handle_tries < total_tries:
            data_handle_error = self.handle_data(file_name)
            if data_handle_error:
                data_handle_tries += 1
                sleep(data_handle_tries * 3)
                continue
            break

        if data_handle_error:
            self.set_job_error(CRAWLER_JOB_TYPE, f"{data_handle_error}", execution_at=execution_time)
            return
        
        # aggregatetion job
        aggregate_error = None
        aggregate_tries = 0

        while aggregate_tries < total_tries:
            aggregate_error = self.handle_aggregate(file_name)
            if aggregate_error:
                aggregate_tries += 1
                sleep(aggregate_tries * 2)
                continue
            break

        if aggregate_error:
            self.set_job_error(CRAWLER_JOB_TYPE, f"{aggregate_error}", execution_at=execution_time)
            return

        self.set_job_success(CRAWLER_JOB_TYPE, execution_at=execution_time)
        self.handle_delete_file(file_name)

CRAWLER_WORKER = DataCrawlerWorker()
