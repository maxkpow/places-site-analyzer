import time
import os
import pandas as pd

def to_excel(result: dict, sitename: str):
    working_folder: str = os.getcwd()

    with pd.ExcelWriter(os.path.join(working_folder, f"{sitename}-analysis-{time.time()}.xlsx")) as writer:
        for content_type, content_list in result.items():
            if len(content_list) > 0:
                df = pd.DataFrame(content_list)
                df.to_excel(writer, sheet_name=content_type)