import pandas as pd
import gzip
import time
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from typing import List
from constants.contenttypes import CONTENT_TYPES
from models.response import HTTPResponse

def decode_gzip_content(content):
    try:
        content = gzip.decompress(content).decode("utf-8")
    except:
        pass
    
    return content

def capture_http_requests(requests) -> HTTPResponse:

    for request in requests:
        if request.response:
            try:
                content_type = request.response.headers['content-type']
                relevent_content_exists = any(map(lambda x: x in content_type, CONTENT_TYPES))
                # relevent_content_exists = True

                if relevent_content_exists:
                    content_encoding = request.response.headers['content-encoding']
                    response_body = decode_gzip_content(request.response.body) if content_encoding == "gzip" else request.response.body 

                    captured_request: HTTPResponse = {
                        "host": request.host,
                        "url": request.url, 
                        "path": request.path,
                        "method": request.method,
                        "headers": dict((key, value) for key, value in request.response.headers.items()),
                        "status": int(request.response.status_code),
                        "content_encoding": content_encoding,
                        "content_type": content_type,
                        "content_length": int(request.response.headers["content-length"]),
                        "body": response_body,
                    }

                    yield captured_request
            except:
                pass

def run_driver(website) -> List[HTTPResponse]:
    
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
   
    driver.get(website)
    
    # Wait 8 seconds for websites that load long time
    # time.sleep(15)

    captured_http_requests: List[HTTPResponse] = list(capture_http_requests(driver.requests))

    driver.quit()

    return captured_http_requests


def generate_api_report(website):    
    
    captured_requests = run_driver(website)
    
    df = pd.DataFrame(captured_requests)
    df.to_excel(f"captured_requests-{time.time()}.xlsx")


if __name__ == "__main__":
    url = "https://www.wildberries.ru/services/besplatnaya-dostavka?desktop=1#terms-delivery"
    generate_api_report(url)