from urllib.parse import urlparse
import pandas as pd
import time
from scany.core import WebDataCapture
import os

def save_result(result: dict, sitename: str):

    output_folder: str = "output"
    
    if output_folder not in os.listdir():
        os.makedirs(output_folder)

    with pd.ExcelWriter(os.path.join(output_folder, f"{sitename}-analysis-{time.time()}.xlsx")) as writer:
        for content_type, content_list in result.items():
            if len(content_list) > 0:
                df = pd.DataFrame(content_list)        
                df.to_excel(writer, sheet_name=content_type)  
        
if __name__ == "__main__":
    
    url = "https://benu.rs/apoteke"
    sitename = urlparse(url).netloc

    wdc = WebDataCapture()
    result = wdc.start(website=url, timeout=3)

    save_result(result, sitename)