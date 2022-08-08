from seleniumwire import webdriver
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import gzip

def decode_gzip_content(content):
    content = gzip.decompress(content).decode("utf-8")
    return content

def capture_http_requests(driver):
    for request in driver.requests:
        if request.response:
            content_encoding = request.response.headers['content-encoding']
            response_body = decode_gzip_content(request.response.body) if content_encoding == "gzip" else request.response.body 

            captured_request = {
                "host": request.host,
                "url": request.url, 
                "path": request.path,
                "method": request.method,
                "headers": [f"{key}: {value}" for key, value in request.headers.items()],
                "response_status": request.response.status_code,
                "response_content_encoding": content_encoding,
                "response_content_type": request.response.headers['content-type'],
                "response_body": response_body,
            }

            yield captured_request

options = webdriver.ChromeOptions()
options.add_argument("--headless")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

driver.get('https://avoska.ru/shops/')

captured_requests = list(capture_http_requests(driver))

df = pd.DataFrame(captured_requests)
df.head()

df.to_excel("captured_requests.xlsx")