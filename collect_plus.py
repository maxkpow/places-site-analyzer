from urllib.parse import urlparse
import pandas as pd
import time
from analyzer.capture import WebDataCapture

url = "https://www.collectplus.yodel.co.uk/click-and-collect"
site_name = urlparse(url).netloc

wdc = WebDataCapture()
result = wdc.start(website=url, timeout=3)

df_req = pd.DataFrame(result['requests'])
df_req.to_excel(f"{site_name}-requests-{time.time()}.xlsx")

df_ol = pd.DataFrame(result['olists'])
df_ol.to_excel(f"{site_name}-olists-{time.time()}.xlsx")

df_ul = pd.DataFrame(result['ulists'])
df_ul.to_excel(f"{site_name}-ulists-{time.time()}.xlsx")

df_js = pd.DataFrame(result['scripts'])
df_js.to_excel(f"{site_name}-scripts-{time.time()}.xlsx")

df_js = pd.DataFrame(result['links'])
df_js.to_excel(f"{site_name}-links-{time.time()}.xlsx")