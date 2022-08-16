from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from scany.models import HTTPResponse
from scany.parsers import HTTPParser, ScriptsParser, ListsParser, LinksParser
from typing import List
import time
import logging

logging.basicConfig(encoding='utf-8', level=logging.INFO)

class WebDataCapture():

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")
        self.options.add_argument("--remote-debugging-port=9222")

        logging.info(msg="Initializing Webdriver options...")
    
    def start(self, website=None, timeout=5):
        self.website = website

        logging.info(msg=f"Start capturing data from {self.website}")

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
        driver.get(website)

        time.sleep(timeout)

        captured_requests: List[HTTPResponse] = self.__parse_requests(driver.requests)
        captured_scripts: List = self.__parse_scripts(driver.find_elements(By.TAG_NAME, "script"))
        captured_olists: List = self.__parse_lists(driver.find_elements(By.TAG_NAME, "ol"))
        captured_ulists: List = self.__parse_lists(driver.find_elements(By.TAG_NAME, "ul"))
        captured_links: List = self.__parse_links(driver.find_elements(By.TAG_NAME, "a"))

    
        # capture all data depending on required content: http, tables, lists, scripts, ect.
        driver.quit()
        logging.info(msg="Webdriver work finished successfully.")
        logging.info(msg="Quit Webdriver.")

        return {
            "requests": captured_requests,
            "olists": captured_olists,
            "ulists": captured_ulists,
            "tables": [],
            "links": captured_links,
            "scripts": captured_scripts
        }
    
    def __parse_requests(self, requests: List):
        logging.info(msg="capturing HTTP Requests...")

        parser = HTTPParser()
        parsed_list = list(parser.parse(requests))

        return parsed_list
    
    def __parse_scripts(self, scripts):
        logging.info(msg="capturing <script>...</script> tags ...")
        parser = ScriptsParser()
        parsed_list = list(parser.parse(scripts, self.website))

        return parsed_list
    
    def __parse_lists(self, html_lists):
        logging.info(msg="capturing <ol>...</ol> & <ul>...</ul> tags ...")
        
        parser = ListsParser()
        parsed_list = list(parser.parse(html_lists))

        return parsed_list
    
    def __parse_links(self, links_list):
        logging.info(msg="capturing <a>...</a> tags ...")
        parser = LinksParser()
        parsed_list = list(parser.parse(links_list, self.website))

        return parsed_list