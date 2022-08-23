import time
import os
import pandas as pd
import logging

def to_excel(result: dict, sitename: str):
    logging.info(msg="Start saving data to Excel...")
    
    working_folder: str = os.getcwd()
    path_to_file = os.path.join(working_folder, f"{sitename}-analysis-{time.time()}.xlsx")

    with pd.ExcelWriter(path_to_file) as writer:
        for content_type, content_list in result.items():
            if len(content_list) > 0:
                df = pd.DataFrame(content_list)
                df.to_excel(writer, sheet_name=content_type)
        
        logging.info(msg="Data successfully saved to Excel...")
        logging.info(msg=f"Path to file: {path_to_file}")