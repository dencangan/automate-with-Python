import os
import json
import time

import pandas as pd
from arctic import Arctic
from selenium import webdriver

default_download_dir = r"C:\Users\Dencan Gan\Downloads"
edcc_link = "https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide.xlsx"

file_name = "COVID-19-geographic-disbtribution-worldwide.xlsx"
file_dir = os.path.join(default_download_dir, file_name)

if os.path.exists(file_dir):
    os.remove(file_dir)

# Starting up selenium...
driver = webdriver.Chrome()
driver.get(edcc_link)
time.sleep(1)
driver.close()

if os.path.exists(file_dir):
    print(f"File downloaded successfully!")

df_global = pd.read_excel(file_dir)

# Arctic storage
# Secret credentials stored locally
mongo_credentials = json.load(open(r"C:\Users\Dencan Gan\Credentials\credentials.json"))["mongodb"]

# Connect to arctic database
a = Arctic(f"mongodb+srv://{mongo_credentials['username']}:{mongo_credentials['password']}@personaldatabase-rgdhs.azure.mongodb.net/test?retryWrites=true&w=majority")
covid19_lib = a["covid19"]

# Upload data
covid19_lib.write("global_data", df_global)
