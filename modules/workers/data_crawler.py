import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time

from selenium.webdriver.chrome.options import Options

driver_options = Options()
driver_options.add_argument("--headless=new")

class DataCrawlerWorker:
    USER_NAME = "PDVIP"
    PASSWORD = "USIVIP@2025"
    URL = "http://10.53.232.80/#/"

    def __init__(self):
        self.driver = None

    def stop(self):
        if self.driver:
            self.driver.quit()

    def execute(self):
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
        first_elem = self.driver.find_element(By.XPATH, './/*[@id="body"]/div[9]/div[1]/div/div[1]/p[1]')
        print(first_elem.text)

        self.driver.quit()

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
