import pandas as pd
from urllib.parse import urlparse
import time
from analyzer.capture import WebDataCapture

class TestCapture():
    def test_avoska(self):
        test_url = "https://avoska.ru/shops/"
        site_name = urlparse(test_url).netloc

        wdc = WebDataCapture()
        result = wdc.start(test_url, timeout=2)

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

        assert len(result) > 0
    

    # def test_wildberries(self):
    #     test_url = "https://www.wildberries.ru/services/besplatnaya-dostavka?desktop=1#terms-delivery"
    #     site_name = urlparse(test_url).netloc

    #     wdc = WebDataCapture()
    #     result = wdc.start(test_url, timeout=30)['requests']

    #     df = pd.DataFrame(result)
    #     df.to_json(f"{site_name}-requests-{time.time()}.xlsx")

    #     assert len(result) > 0