import os

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from libs.manage_yaml import open_yaml


def check_connection(url: str) -> [bool, str]:
    x = requests.get(url=url)
    if x.status_code == 200:
        return True, None
    else:
        return False, x.status_code


class Host:

    def __init__(self):
        self.yaml = open_yaml()
        self.driver = webdriver.Chrome(executable_path=os.getcwd() + self.yaml['chrome_path'])

    # Check if the site is connecting

    def open_browser(self):
        self.driver.implicitly_wait(30)
        self.driver.delete_all_cookies()
        self.driver.maximize_window()

    def go_to_page(self, url):
        self.driver.get(url)

    def close_browser(self):
        self.driver.quit()

    def login_page(self, user: str, password: str):
        self.driver.find_element_by_xpath(self.yaml['login_page']['user']).send_keys(user)
        self.driver.find_element_by_xpath(self.yaml['login_page']['password']).send_keys(password)
        self.driver.find_element_by_xpath(self.yaml['login_page']['login_button']).click()

    def search_projects(self, search_criteria):
        self.driver.find_element_by_id(self.yaml['project_page']['search_project']).clear()
        self.driver.find_element_by_id(self.yaml['project_page']['search_project']).send_keys(
            search_criteria + Keys.RETURN)

    def get_projects_list(self):
        return self.driver.find_elements_by_xpath(self.yaml['project_page']['projects_list'])

    def wait_element(self, by: By, e):
        try:
            element_present = EC.presence_of_element_located((by, e))
            WebDriverWait(self.driver, 10).until(element_present)
            return True
        except TimeoutException:
            return False

    def verify_page(self, title: str):
        return self.driver.title == title
