# !pip install selenium
# !brew install chromedriver
# update your Chrome version

import parameters
import requests, sys
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
from bs4 import BeautifulSoup

PATH_TO_CHROMEDRIVER = 'C:\\Users\\ssingh\\Downloads\\chromedriver_win32\\chromedriver.exe'
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
            company_url = "https://www.linkedin.com/company/sampson-construction"
            people_url = company_url + "/people/"
            self.driver.get(people_url)

            """
            # Wait for the "People" page to load (optional)
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'org-people-search')]")))

            search_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
            search_button.send_keys('Sampson Construction Co')
            search_button.send_keys(Keys.RETURN)
            # Wait for the search results to load
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(@class, 'entity-result__title-text')]//a[@data-test-app-aware-link]")))

            # Click on the first search result
            first_result = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'entity-result__title-text')]//a[@data-test-app-aware-link][1]")))
            first_result.click()
            sleep(2)

            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'org-top-card')]")))

            # Click on the "People" element
            people_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'org-page-navigation__item-anchor') and contains(text(), 'People')]")))
            people_link.click()

            # Wait for the "People" page to load (optional)
            self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'org-people-search')]")))

            connections_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Connections']")))
            connections_button.click()
            sleep(0.5)
            checkbox = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='network-F']")))
            checkbox.click()
            # sleep(0.5)
            # checkbox = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='network-S']")))
            # checkbox.click()
            sleep(1)
            show_result_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Show results']")))
            show_result_button.click()
            sleep(3)
            #profile_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'entity-result__title-text')]//a")))
            #profile_link.click()
            """
        except:
            print('SEARCH FAILED')

    def get_about_info(self, sel):
        """
        Extracts information from the "About" section of a LinkedIn profile
        :param sel: a "Selector" object from python "Parser" library
        :return: extracted information
        """
        try:
            about_section = self.driver.find_element(by=By.XPATH, value='//*[text()="About"]')
        except:
            about_section = False

        if about_section:
            # navigate About element into the center of view
            self.scroll_to_element(about_section)

            about = sel.xpath('//section[descendant::text()="About"]/*//span[@aria-hidden="true"]'
                              '//text()[normalize-space()]').getall()
            sleep(3)
            about = '\n'.join(about[1:])
        else:
            about = ''
        return about

    def get_experience_info_regular(self, job, experience):
        """
        Extracts 'Experience' info of a regular representation: one job title for a given company (job parameter)
        :param job: xpath to a single company
        :param experience: list of a candidate's experiences
        :return: experience
        """

        description = job.xpath(
            '*//div[@class="pvs-list__outer-container"]//span[@aria-hidden="true"]//text()[normalize-space()]').getall()
        if not description:
            description = ''

        info = job.xpath('*//span[@aria-hidden="true"]//text()[normalize-space()]').getall()
        info = [i for i in info if i not in description]

        job_title = info[0]

        company_name = (info[1].split(' · '))[0]

        date = info[2].split(' · ')[0].split(' - ')
        if len(date) == 2:
            date_start, date_end = date[0], date[1]
        else:
            date_start, date_end = date[0], date[0]

        try:
            job_location = info[3]
        except IndexError:
            job_location = ''

        if not description:
            description = ''
        else:
            description = '\n '.join(description)

        experience += [[job_title, company_name, date_start, date_end, job_location, description]]

        return experience

    def get_experience_info_special(self, job, experience, show_all):
        """
        Extracts 'Experience' info of a special representation: several job titles for a given company (job parameter)
        :param job: xpath to a single company
        :param experience: list of a candidate's experiences
        :param show_all: if a displayed list of candidate's experience is not full on a profile page and was expanded
         by clicking the "Show all experiences".
        :return: experience
        """

        # get company info
        company_name = job.xpath('*//text()[normalize-space()]').get()
        if not show_all:
            titles_xpath = job.xpath(
                '*/*/*[@class="pvs-list__outer-container"]/*/li')
        else:
            titles_xpath = job.xpath(
                '(//text()[contains(.,"Experience")]/ancestor::*[self::section]//ul)[1]/li//li[contains(@class, "paged-list-item")]')

        for title in titles_xpath:
            description = title.xpath(
                './/*[@class="pvs-list__outer-container"]//text()[normalize-space()]').get()
            if not description:
                description = ''

            info = title.xpath('.//span[@aria-hidden="true"]//text()[normalize-space()]').getall()
            info = [i for i in info if i not in description]

            job_title = info[0]
            for i in range(1, len(info)):
                if any(l.isdigit() for l in info[i]):
                    date = info[i].split(' · ')[0].split(' - ')
                    try:
                        job_location = info[i + 1]
                    except IndexError:
                        job_location = ''

            # parse date
            if len(date) == 2:
                date_start, date_end = date[0], date[1]
            else:
                date_start, date_end = date[0], date[0]

            experience += [[job_title, company_name, date_start, date_end, job_location, description]]

        return experience

    def get_experience_info(self, sel):
        """
        Extracts information from the "Experience" section of a candidate's profile
        :param sel: a "Selector" object from python "Parser" library
        :return: extracted information
        """
        wait = WebDriverWait(self.driver, 1)
        try:
            experience_section = self.driver.find_element(by=By.XPATH, value='//*[text()="Experience"]')
        except:
            experience_section = False

        if experience_section:
            # navigate Experience element into the center of view
            self.scroll_to_element(experience_section)

            # detect whether "Show all {n} experiences" 'button' exist. If does, one must click to extend the list
            # of experiences
            try:
                show_all_button = wait.until(EC.element_to_be_clickable((By.XPATH,
                                    '//section[descendant::text()="Experience"]//*[text()[contains(., "Show all" )]]')))
                show_all = 1
            except:
                show_all = 0

            # find xpath to 'Experience' section if exist (job_xpath)
            if show_all:
                sleep(0.5)
                show_all_button.click()
                sleep(1)
                self.scroll_page(5)
                sel = Selector(text=self.driver.page_source)
                job_xpath = sel.xpath('(//text()[contains(.,"Experience")]/ancestor::*[self::section]//ul)[1]/li')
            else:
                sleep(3)
                job_xpath = sel.xpath(
                    '//section[descendant::text()="Experience"]/*[@class="pvs-list__outer-container"]/*/li')

            # parse the Experience section
            experience = []
            for job in job_xpath:
                # determine if displayed experience is of a special case (several job titles within a company)
                special_representation = 0
                if job.xpath('*//span[@class="pvs-entity__path-node"]'):
                    special_representation = 1

                if special_representation:
                    experience = self.get_experience_info_special(job, experience, show_all)
                else:
                    experience = self.get_experience_info_regular(job, experience)

            if show_all:
                self.driver.back()
                sleep(1)

        else:
            experience = ['', '', '', '', '', '']

        return experience

    def get_education_info(self, sel):
        """
        Extracts information from the "Education" section of a LinkedIn profile
        :param sel: a "Selector" object from python "Parser" library
        :return: extracted information
        """
        wait = WebDriverWait(self.driver, 1)

        try:
            education_section = self.driver.find_element(by=By.XPATH, value='//*[text()="Education"]')
        except:
            education_section = False

        if education_section:
            # navigate Education element into the center of view
            self.scroll_to_element(education_section)

            # detect whether "Show all {n} experiences" 'button' exist. If does, then one must click to extend the list
            # of experiences
            try:
                show_all_button = wait.until(EC.element_to_be_clickable((By.XPATH,
                                    '//section[descendant::text()="Education"]//*[text()[contains(., "Show all" )]]')))
                show_all = 1
            except:
                show_all = 0

            # find xpath to 'Education' section if exist (job_xpath)
            if show_all:
                sleep(0.7)
                show_all_button.click()
                sleep(1)
                self.scroll_page(5)
                sel = Selector(text=self.driver.page_source)
                education_xpath = sel.xpath('(//text()[contains(.,"Education")]/ancestor::*[self::section]//ul)[1]/li')
            else:
                sleep(2)
                education_xpath = sel.xpath(
                    '//section[descendant::text()="Education"]/*[@class="pvs-list__outer-container"]/*/li')

            education = []
            for ed in education_xpath:
                description = ed.xpath(
                                        '*//div[@class="pvs-list__outer-container"]//span[@aria-hidden="true"]'
                                        '//text()[normalize-space()]').getall()
                if not description:
                    description = ''
                info = ed.xpath('*//span[@aria-hidden="true"]//text()[normalize-space()]').getall()
                info = [i for i in info if i not in description]

                school_name = info[0]

                # Fields 'degree/department' and 'date_start/date_end' are optional and might be empty. The following
                # logic helps identify them correctly.

                info_len = len(info)

                if info_len == 1:
                    degree_department = ''
                    date = ''
                elif info_len == 2:
                    if any(i.isdigit() for i in info[1]):
                        date = info[1]
                        degree_department = ''
                    else:
                        degree_department = info[1]
                        date = ''
                else:
                    degree_department = info[1]
                    date = info[2]

                if len(degree_department) == 2:
                    degree, department = degree_department.split(', ')
                else:
                    degree, department = degree_department, ''

                date = date.split(' - ')
                if len(date) == 2:
                    date_start = date[0]
                    date_end = date[1]
                else:
                    date_start = date[0]
                    date_end = date[0]

                if not description:
                    description = ''
                else:
                    description = '\n '.join(description)
                education += [[school_name, degree, department, date_start, date_end, description]]

            if show_all:
                self.driver.back()
                sleep(1)
        else:
            education = ['', '', '', '', '', '']
        print("Education Information:", education)
        return education

    def get_main_info(self, sel):
        """
        Extracts main information: name, job_title, location and from the "About", "Experience" and "Education" sections
        of a LinkedIn profile
        :param sel: a "Selector" object from python "Parser" library
        :return: extracted information
        """
        main = []

        name = sel.xpath('//*[starts-with(@class, "text-heading-xlarge")]/text()').get()
        job_title = sel.xpath('//*[starts-with(@class, "text-body-medium")]/text()').get()
        location = sel.xpath('//*[starts-with(@class, "text-body-small")]/text()').get()

        name = str_strip(name)
        job_title = str_strip(job_title)
        location = str_strip(location)

        profile_picture_url = sel.xpath('//img[contains(@class, "profile-picture")]/@src').get()
        # urllib.request.urlretrieve(profile_picture_url, name + '.jpg')
        profile_picture = bytearray(requests.get(profile_picture_url).content)

        # About
        about = self.get_about_info(sel)

        main += [name, job_title, location, about, profile_picture]

        # Experience
        experience = self.get_experience_info(sel)
        main += [experience]

        # Education
        education = self.get_education_info(sel)
        main += [education]

        return main

    def get_contact_info(self, sel):
        """
        Extracts contact information: profile url, website, phone number and e-mail of a LinkedIn profile
        :param sel: a "Selector" object from python "Parser" library
        :return: extracted information
        """

        contact = []

        self.wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[text()="Contact Info"]')))

        url = sel.xpath('//section[@class="pv-contact-info__contact-type ci-vanity-url"]//a/@href').getall()
        if url:
            url = [w.strip() for w in url]
            url = [w for w in url if '@' or '(at)' in w]
            url += ['']
            url = ' '.join(url)
            url = url.strip()
        else:
            url = ''

        website = sel.xpath('//section[@class="pv-contact-info__contact-type ci-websites"]'
                            '//*[starts-with(@class,"pv-contact-info__ci-container")]//text()[normalize-space()]').getall()
        if website:
            website = [w.strip() for w in website]
            website = [w for w in website if '.' in w]
            website += ['']
            website = ' '.join(website)
            website = website.replace(' ', '')
            website = website.strip()
        else:
            website = ''

        phone = sel.xpath('//section[@class="pv-contact-info__contact-type ci-phone"]'
                          '//*[starts-with(@class,"pv-contact-info__ci-container")]//text()[normalize-space()]').getall()
        if phone:
            phone = [w.strip() for w in phone]
            phone = [w for w in phone if any(i.isdigit() for i in w)]
            phone += ['']
            phone = ' '.join(phone)
            phone = phone.replace(' ', '')
            phone = phone.strip()
        else:
            phone = ''

        email = sel.xpath('//section[@class="pv-contact-info__contact-type ci-email"]'
                          '//*[starts-with(@class,"pv-contact-info__ci-container")]//text()[normalize-space()]').getall()
        if email:
            email = [w.strip() for w in email]
            email = [w for w in email if '@' or '(at)' in w]
            email += ['']
            email = ' '.join(email)
            email = email.strip()
        else:
            email = ''

        contact = [url, website, phone, email]

        return contact

    def get_full_info(self):
        """
        Extracts all the information from LinkedIn profile
        :return: profile info (name, contact, education, experience, etc.)
        """

        info = []

        sel = Selector(text=self.driver.page_source)

        # get the main info
        main_info = self.get_main_info(sel)
        info += main_info
        print("Main Information:", main_info)
        # get contact info
        sleep(2)
        self.driver.execute_script("window.scrollTo({'top': 0, 'left': 0, 'behavior': 'smooth'})")
        sleep(2)
        contact_info_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Contact info']")))
        contact_info_button.click()
        sleep(3)

        sel = Selector(text=self.driver.page_source)

        contact_info = self.get_contact_info(sel)
        print("Contact Information:", contact_info)
        self.driver.back()
        sleep(1)

        info += contact_info

        return info

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
