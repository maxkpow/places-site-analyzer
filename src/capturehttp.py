import pandas as pd
import gzip
import time
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
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
            content_type = request.response.headers['content-type']
            relevent_content_exists = any(map(lambda x: x in content_type, CONTENT_TYPES))

            if relevent_content_exists:
                content_encoding = request.response.headers['content-encoding']
                response_body = decode_gzip_content(request.response.body) if content_encoding == "gzip" else request.response.body 

                captured_request: HTTPResponse = {
                    "host": request.host,
                    "url": request.url, 
                    "path": request.path,
                    "method": request.method,
                    "headers": [f"{key}: {value}" for key, value in request.headers.items()],
                    "response_status": int(request.response.status_code),
                    "response_content_encoding": content_encoding,
                    "response_content_type": content_type,
                    "response_body": response_body,
                }

                yield captured_request

def run_driver(website) -> List[HTTPResponse]:
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(website)

    captured_http_requests: List[HTTPResponse] = list(capture_http_requests(driver.requests))

    driver.quit()

    return captured_http_requests


def generate_api_report(website):    
    
    captured_requests = run_driver(website)
    
    df = pd.DataFrame(captured_requests)
    df.to_excel(f"captured_requests-{time.time()}.xlsx")


if __name__ == "__main__":
    url = "https://pydantic-docs.helpmanual.io/usage/schema/"
    generate_api_report(url)