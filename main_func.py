from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
from datetime import datetime


def login(login, pwd):  # login to target website
    username = driver.find_element(By.ID, "emailForm_email-input")  # fill login
    username.clear()
    username.send_keys(str(login))
    password = driver.find_element(By.ID,"emailForm_password-input")  # fill password
    password.clear()
    password.send_keys(str(pwd))
    driver.find_element(By.ID, "emailForm_submit").click()  # click submit


def extract_table():  # extract hole table with reports, to find index row of our 'TMPO_1' report
    driver.find_element(By.CSS_SELECTOR, "div[id='x-auto-30'] div div[class='trigger']").click()    # click on triiger to change 500 rows in a table
    driver.find_element(By.CSS_SELECTOR, "div[class='tpwE-E'] div:nth-child(6)").click()  # click on 500 rows
    time.sleep(1)
    webtable_df = pd.read_html(driver.find_element(By.XPATH, "//div[@id='reportingProfileGridPanelId_listGrid']"  # download to dataframe table from website 
                                                            "//table[@class='tpwNFE gridData']").get_attribute('outerHTML'))[0]
    time.sleep(1)
    #  webtable_df.rename(columns={'Unnamed: 0': 'checkbox', 'Unnamed: 1': 'report_name','Unnamed: 2': 'last_changes', 'Unnamed: 3': 'staff','Unnamed: 4': 'added', 'Unnamed: 5': 'who_add', 'Unnamed: 6': 'permission'}, inplace=True)
    TMPO_index = webtable_df.index[webtable_df['Unnamed: 1'] == 'TMPO_1'] + 1   # index row of need report
    return TMPO_index


if __name__ == "__main__":
    while True:
        try:
            driver_path = Service("chromedriver.exe")   # path to driver
            driver = webdriver.Chrome(service=driver_path)
            #  driver = webdriver.Chrome(ChromeDriverManager().install())   uncomment if you dont have Chrome driver,
                                                                         #  then change the path
            driver.maximize_window()
            driver.get("https://login.transporeon.com/#ReportingDataWarehouse")  # open web
            #driver.get("https://login.transporeon.com/login/")
            time.sleep(2)
            login(login="-----", pwd="-----")
            time.sleep(15)
            TMPO_index = extract_table()
            time.sleep(1)
            driver.find_element(By.XPATH, "//tbody/tr[" + str(TMPO_index[0]) + "]/td[1]/div[1]/div[1]").click()  # click on need report
            time.sleep(1)
            driver.find_element(By.ID, "generateReport").click()  # click on generate report button
            time.sleep(35)
            driver.close()
            break
        except Exception as e:

            with open('log.txt', 'a') as log_file:
                log_file.write(str(datetime.date(datetime.now())) + " " + str(datetime.time(datetime.now())) + '\n')
                log_file.write(str(e))
                log_file.close()
