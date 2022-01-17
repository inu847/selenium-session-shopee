from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import sleep
import time
from random import randint
import json
import string
import requests
import os
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Read Data in Config
user = open(r"data/config.json", "r")
dataJsons = json.load(user)
emailConfig = dataJsons['lisensi']['email']
passwordConfig = dataJsons['lisensi']['pwd']
userAgentConfig = dataJsons['lisensi']['user-agent']
accesToken = dataJsons['lisensi']['access-token']

# SETTING
BASE_SESSION = dataJsons['path_session']

def main():
    os.system("cls")
    username = input("Masukkan Username : ")

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox");
    chrome_options.add_argument("start-maximized");
    chrome_options.add_argument("disable-infobars");
    chrome_options.add_argument("--disable-extensions");
    chrome_options.add_argument("--disable-gpu");
    chrome_options.add_argument("--disable-dev-shm-usage");
    chrome_options.add_argument("--user-data-dir=" + BASE_SESSION + username)

    PATH = 'data/chromedriver'
    driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
    driver.get("https://shopee.co.id/")


if __name__ == '__main__':
    try:
        os.mkdir("session")
    except:
        pass

    conditionConfig = False
    try:
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("data/config-cd7413190612.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("config").sheet1
        datas = sheet.get_all_records()

        for data in datas:
            email = data['Email']
            password = data['Password']
            userAgent = data['User Agent']
            status = data['Status']
            token = data['Token']

            if email == emailConfig and password == passwordConfig and userAgent == userAgentConfig and status == 'Active' and accesToken == token:
                print('Login config success!!')
                conditionConfig == True
                action = "1"
                while action != "0":
                    # while True:
                    #     os.system("cls")
                    #     print("[ INFO ]_main_: session time " + str(time))
                    main()
                    action = input("[ INFO ]_main_: press 0 to quit session and enter to new session")
                #     sleep(1)
                #     time += 1
                driver.quit()
                break
            elif email == emailConfig and password == passwordConfig and userAgent == userAgentConfig and status != 'Active' and accesToken == token:
                print('Login Failed!! Your Config non-active')
                sleep(3)
                # else:
                # print(userAgent+"\n"+userAgentConfig)
    except:
        pass

    if conditionConfig == False:
        print('[ INFO ]__main__ : Login Failed!!')
        sleep(3)