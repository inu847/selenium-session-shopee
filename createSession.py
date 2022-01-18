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
import datetime

# Read Data in Config
user = open(r"data/config.json", "r")
dataJsons = json.load(user)
emailConfig = dataJsons['lisensi']['email']
passwordConfig = dataJsons['lisensi']['pwd']
userAgentConfig = dataJsons['lisensi']['user-agent']
accesToken = dataJsons['lisensi']['access-token']

# SETTING
BASE_SESSION = dataJsons['path_session']

def verivyHotmail(driver, userHotmail, passrHotmail):
    driver.execute_script('window.open("https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1639366524&rver=7.0.6737.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fnlp%3d1%26RpsCsrfState%3d7acc44a4-9441-dc05-d889-cd9a3cfb9351&id=292841&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=90015","_blank");')
    driver.implicitly_wait(10)

    # driver.get(
    #     "https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1639366524&rver=7.0.6737.0&wp=MBI_SSL&wreply=https%3a%2f%2foutlook.live.com%2fowa%2f%3fnlp%3d1%26RpsCsrfState%3d7acc44a4-9441-dc05-d889-cd9a3cfb9351&id=292841&aadredir=1&CBCXT=out&lw=1&fl=dob%2cflname%2cwld&cobrandid=90015")
    driver.switch_to.window(driver.window_handles[1])
    print("[ INFO ]__main__: Verivy hotmail " + userHotmail)
    try:
        inputUser = driver.find_element_by_name("loginfmt")
        inputUser.send_keys(userHotmail)
        inputUser.send_keys(Keys.ENTER)
        driver.implicitly_wait(10)

        inputPassword = driver.find_element_by_name("passwd")
        inputPassword.send_keys(passrHotmail)
        driver.implicitly_wait(10)
        try:
            driver.find_element_by_xpath('//*[@value="Sign in"]').click()
            # driver.execute_script("arguments[0].click();", btnSingin)
        except:
            inputPassword.send_keys(Keys.ENTER)
        driver.implicitly_wait(10)

        try:
            driver.find_element_by_id("idBtn_Back").click()
            driver.implicitly_wait(20)
            try:
                driver.find_element_by_id("O365_MainLink_MePhoto")
                driver.get("https://outlook.live.com/mail/0/junkemail")
            except:
                pass
        except:
            pass
        input("[ INFO ]__main__: Account Has Verivied")
    except:
        input("[ INFO ]__main__: Login " + userHotmail + " Gagal")

    

def login(userHotmail, passrHotmail, username, password):
    chrome_options = Options()
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        chrome_options.add_argument("--user-data-dir=" + BASE_SESSION + username)
    except:
        hashInt = randint(1, 100)
        chrome_options.add_argument("--user-data-dir=" + BASE_SESSION + username + hashInt)

    PATH = 'data/chromedriver.exe'
    driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
    driver.get('https://shopee.co.id/user/account/profile')
    driver.implicitly_wait(20)

    try:
        users = driver.find_element_by_name("loginKey")
        users.send_keys(username)
        driver.implicitly_wait(20)

        passwd = driver.find_element_by_name("password")
        passwd.send_keys(password)
        driver.implicitly_wait(20)

        passwd.send_keys(Keys.RETURN)
        driver.implicitly_wait(10)

        try:
            driver.implicitly_wait(10)
            driver.find_element_by_xpath('//*[text()="Verifikasi dengan link email"]')
            driver.find_element_by_xpath('//*[@class="WMREvW"]').click()
            verivyHotmail(driver, userHotmail, passrHotmail)
            driver.switch_to.window(driver.window_handles[0])
        except:
            pass

        profileAccount = driver.find_element_by_xpath('//*[@class="navbar__username"]').text
        print("[ INFO ]__main__: Logged in " + profileAccount)
        print(f"[ INFO ]__main__: create session {username}")
        writers = open('status.txt', 'a+', encoding="utf-8")
        writers.writelines(f"{username}|{password}|Success\n")
        writers.close()
    except:
        print("[ INFO ]__main__: Login Failed")
        print(f"[ INFO ]__main__: failed create session {username}")
        writers = open('status.txt', 'a+', encoding="utf-8")
        writers.writelines(f"{username}|{password}|Failed\n")
        writers.close()
        driver.quit()
        return False

    driver.quit()

def main():
    jadwal = input("Post Penjadwalan y/n ")
    if jadwal == "y":
        link = input("Masukkan Jadwal Waktu Post *format(jam:menit) : ")

    if link:
        times_flashSale = link.split(":")
        hI = int(times_flashSale[0])
        mI = int(times_flashSale[1])
        # WAIT STORE
        while True:
            sleep(0.5)
            x = datetime.datetime.now()
            h = int(x.strftime("%H"))
            m = int(x.strftime("%M"))
            s = int(x.strftime("%S"))
            rate_hourse = hI - h
            rate_minuite = mI - m
            rate_second = 0 - s
            hourse_second = rate_hourse * 3600
            minute_second = rate_minuite * 60

            limit = hourse_second + minute_second + rate_second
            refresh = limit % 2
            
            os.system('cls')
            dateTimeObj = datetime.datetime.now()
            timestampStr = dateTimeObj.strftime("%H:%M:%S")
            print("[", timestampStr, "]""[INFO :] " + str(limit) + " second")

            if limit <= 0:
                print("finished!!")
                break

    account = open('akun.txt')
    accounts = account.readlines()
    lengthAccount = len(accounts) + 1

    for (akun, i) in zip(accounts, range(0, lengthAccount)):
        print(f"[ INFO ]__main__: in progress {i + 1}/{lengthAccount}")
        accountStrip = akun.strip()
        userHotmail = accountStrip.split("|")[0]
        passrHotmail = accountStrip.split("|")[1]
        username = accountStrip.split("|")[2]
        password = accountStrip.split("|")[3]
        login(userHotmail, passrHotmail, username, password)

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
                main()
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