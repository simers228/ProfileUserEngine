from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from time import sleep

PATH_TO_CHROMEDRIVER = '../chromedriver.exe'
LOGIN_NAME = 'calvinsopocy@gmail.com'
LOGIN_PASSWORD = "6mNnjNL?ha,//$z"

class LinkedInScraper:
    def __init__(self, URL):
        self.login_name = LOGIN_NAME
        self.login_password = LOGIN_PASSWORD
        self.linkedin_url = 'https://www.linkedin.com'
        self.chrome_options = webdriver.ChromeOptions().add_argument('--ignore-certificate-errors --ignore-ssl-errors')
        self.service = Service(PATH_TO_CHROMEDRIVER)
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 60)
        self.URL = URL
    def log_in(self):
        self.driver.get(self.linkedin_url)
        sleep(2)
        try:
            username = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='session_key']")))
            password = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='session_password']")))
            login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
            username.send_keys(self.login_name)
            sleep(2)
            password.send_keys(self.login_password)
            sleep(2)
            login_button.click()
            sleep(2)
            logged_in = True
        except:
            print('LOGIN FAILED')

    def search_profiles(self):
        try:
            sleep(2)
            self.driver.get(self.URL)
        except:
            print('SEARCH FAILED')

    def process(self):
        self.log_in()
        self.search_profiles()

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        profile_links = self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//a[contains(@class, 'app-aware-link') and contains(@href, '/in/')]")))

        all_usernames = []

        for link in profile_links:
            href_value = link.get_attribute('href')
            url_parts = href_value.split('/')
            username = url_parts[-1].split('?')[0]
            all_usernames.append(username)

        unique_usernames = sorted(set(all_usernames))
        return unique_usernames