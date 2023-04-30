import sys
import csv
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from parsel import Selector
from time import sleep

PATH_TO_CHROMEDRIVER = '..\..\chromedriver.exe'
LOGIN_NAME = 'simers228@gmail.com'

LOGIN_PASSWORD = [PASSWORD]
RESULTS_FILE_NAME = 'output'
LINKEDIN_URL = 'https://www.linkedin.com'


from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')

service = Service(PATH_TO_CHROMEDRIVER)
driver = webdriver.Chrome(service=service, options=chrome_options)

def str_strip(var):
    if var:
        var = var.strip()
    else:
        var = ''

    return var


class LinkedInScrapper:

    def __init__(self, driver):
        self.login_name = LOGIN_NAME
        self.login_password = LOGIN_PASSWORD
        self.results_file_name = RESULTS_FILE_NAME
        self.linkedin_url = LINKEDIN_URL
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 60)
        self.column_names = ['name', 'job_title', 'location', 'self_description', 'profile_picture',
                             'Experience = [job_title, company_name, date_start, date_end, job_location, job_description]',
                             'Education = [school_name, degree, department, date_start, date_end, education_description]',
                             'profile_url', 'website', 'phone', 'email']

    def scroll_page(self, num_iterations):
        """Scroll the profile page"""
        y = random.randint(150, 250)
        for i in range(num_iterations):
            sleep(random.uniform(0.2, 0.5))
            self.driver.execute_script(f"window.scrollTo({{'top': {y}, 'left': 0, 'behavior': 'smooth'}})")
            y += y
        sleep(0.5)
        self.driver.execute_script("window.scrollTo({'top':0, 'left':0, 'behavior':'smooth'})")
        sleep(1)

    def scroll_to_element(self, element):
        """
        Scrolls the element into the center of view
        :param element: webdriver page element
        """
        self.driver.execute_script(
            "arguments[0].scrollIntoView({'behavior':'smooth', 'block':'center','inline':'start'})",
            element)
        sleep(1)

    def log_in(self):
        '''
        Log in to LinkedIn in Chrome browser using Selenium
        '''
        # use chromedriver to navigate to LinkedIn
        self.driver.get(self.linkedin_url)
        sleep(2)
        # log in
        try:
            username = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='session_key']")))
            password = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='session_password']")))
            login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
            username.send_keys(self.login_name)
            sleep(1)
            password.send_keys(self.login_password)
            sleep(1)
            login_button.click()
            sleep(2)
        except:
            print('LOGIN FAILED')
    import re
    import time


    def search_profiles(self):
        '''
        Search for profiles with 1st level connections
        '''
        try:
            sleep(2)
            # Assuming you already have your webdriver instance as 'self.driver' and WebDriverWait as 'self.wait'

            # Navigate directly to the company "People" page
            company_url = sys.argv[1]
            people_url = company_url + "/people/"
            self.driver.get(people_url)

            keywords_textbox = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='people-search-keywords']")))
            keywords_textbox.click()
            keywords_textbox.send_keys('sales')
            keywords_textbox.send_keys(Keys.ENTER)
        except:
            print('SEARCH FAILED')

    def process_batch(self, writer, last=False):
        """Extract information from a batch of profiles: a list of profile pages - a result of search.
        Each batch except the last one contains exactly 10 profiles."""
        # One could save all the profile urls into a separate file firsr
        # Instead, we simulate human behaviour as close as possible: scroll to the profile of interest,
        # click on each person's profile, extract information and go back
        urls_len = 0  # Set a default value for urls_len

        try:
            urls = self.wait.until(
    EC.visibility_of_all_elements_located((By.XPATH, "//span[contains(@class, 'entity-result__title-text')]"
                                                    "/a[contains(@class, 'app-aware-link')]")))
            urls_len = len(urls)  # Update the value of urls_len if extraction is successful
        except:
            print('Failed to extract profile urls')
            #print('Page source:', self.driver.page_source)
        else:
            if urls_len != 10 and not last:
                sys.exit('Failed to extract all profile urls')

        if urls_len != 10 and not last:
            sys.exit('Failed to extract all profile urls')

        for i in range(1, urls_len + 1):
            user = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "(//span[contains(@class, 'entity-result__title')]"
                                                          f"/a[@class='app-aware-link'])[{i}]")))
            # scroll the user element into the center of view
            self.scroll_to_element(user)
            sleep(2)

            # click on the user's profile
            user.click()
            sleep(2)
            self.scroll_page(10)
            sleep(1)

            # extract information
            info = self.get_full_info()
            print("Full Profile Information:", info)

            self.driver.back()
            sleep(2)

            writer.writerow(info)

            print("Full Profile Information for user {}: ".format(i), info)


    
    def process(self):
        """
        Process scrapping and saves to an output file
        """

        self.log_in()
        self.search_profiles()

        f = open(self.results_file_name, 'w')
        writer = csv.writer(f)
        writer.writerow(self.column_names)

        all_usernames = []

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to the bottom of the page
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for the new profiles to load
            sleep(3)  # Adjust this value based on the loading time of the profiles

            # Get the new scroll height after loading new profiles
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            # If the scroll height hasn't changed, it means there are no more profiles left to load
            if new_height == last_height:
                break

            last_height = new_height

        # Find all the profile links
        profile_links = self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//a[contains(@class, 'app-aware-link') and contains(@href, '/in/')]")))

        # Extract the usernames from the links
        for link in profile_links:
            href_value = link.get_attribute('href')
            url_parts = href_value.split('/')
            username = url_parts[-1].split('?')[0]
            all_usernames.append(username)

            # Print the username
            print("Username:", username)

        # Print the list of usernames from all pages
        print("All usernames:", all_usernames)

        f.close()

        print('Crawling successfully completed!')

    def remove_duplicates(self):
        file_name = self.results_file_name
        df = pd.read_csv(file_name)
        df = df.drop_duplicates(subset='profile_url', keep="first")
        df.to_csv(file_name, mode='w', header=True, index=False)
        print('Duplicates removed')


# use chromedriver to navigate to LinkedIn
from selenium.webdriver.chrome.service import Service

service = Service(PATH_TO_CHROMEDRIVER)
driver = webdriver.Chrome(service=service)

crawler = LinkedInScrapper(driver)
# get profiles information
crawler.process()

# remove duplicates
crawler.remove_duplicates()

sleep(10)
driver.quit()

""" =================================================================================================================== 
Improve:
- Education info
    degree, department - if one is missing we assign the value to degree; make it more precise 
    (bachelor, master, phd, doctor, etc)
   =================================================================================================================== """
