from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from typing import List
import gzip
import brotli
from analyzer.constants import CONTENT_TYPES, SEARCH_WORDS
from analyzer.models import HTTPResponse
import time

class WebDataCapture():

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")
        self.options.add_argument("--remote-debugging-port=9222")
    
    def start(self, website=None, timeout=5):
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
        driver.get(website)

        # import pdb;pdb.set_trace()
        # timeout for long loading websites & ajax requests
        time.sleep(timeout)

        # capture unordered lists
        captured_ulists = driver.find_elements(By.TAG_NAME, "ul")
        captured_ulists_text = [item.text for item in captured_ulists if item.text != ""]

        # capture ordered lists
        captured_olists = driver.find_elements(By.TAG_NAME, "ol")
        captured_olists_text = [item.text for item in captured_olists if item.text != ""]
        
        # capture scripts
        captured_scripts = driver.find_elements(By.TAG_NAME, "script")
        captured_scripts_text = [item.text for item in captured_scripts if item.text != ""]

        # capture http requests
        captured_http_requests: List[HTTPResponse] = list(self.parse_http_requests(driver.requests))
    
        # capture all data depending on required content: http, tables, lists, scripts, ect.
        driver.quit()

        return {
            "requests": captured_http_requests,
            "olists": captured_olists_text,
            "ulists": captured_ulists_text,
            "tables": [],
            "scripts": captured_scripts_text
        }

    def content_decoder(self, content, content_encoding):
        if content_encoding == "gzip":
            return gzip.decompress(content).decode("utf-8")
        elif content_encoding == "br":
            return brotli.decompress(content).decode("utf-8")
        else:
            return content
    
    def search_words(self, content: str = "") -> bool:
        if any(map(lambda x: x in content.lower(), SEARCH_WORDS)):
            return True
        else:
            return False
    
    def parse_http_requests(self, requests: List):
        for request in requests:
            if request.response:
                try:
                    content_type = request.response.headers['content-type']
                    
                    relevent_content_exists = any(map(lambda x: x in content_type, CONTENT_TYPES))
                    # relevent_content_exists = True

                    if  relevent_content_exists:
                        
                        headers = dict((key, value) for key, value in request.response.headers.items())
                        content_encoding = request.response.headers['content-encoding']
                        response_body = self.content_decoder(request.response.body, content_encoding)
                        location_words = self.search_words(response_body)

                        captured_request: HTTPResponse = {
                            "location_words": location_words,
                            "host": request.host,
                            "url": request.url, 
                            "path": request.path,
                            "method": request.method,
                            "status": request.response.status_code,
                            "headers": headers,
                            "content_encoding": content_encoding,
                            "content_type": content_type,
                            "content_length": request.response.headers["content-length"],
                            "body": response_body,
                        }

                        yield captured_request
                except:
                    pass
