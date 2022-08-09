from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

class Capture():

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")
    
    def start(self, website):
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options)
        driver.get(website)
        # capture all data depending on required content: http, tables, lists, scripts, ect.
        driver.quit()

        return {
            "https": [],
            "lists": [],
            "tables": [],
            "scripts": []
        }
