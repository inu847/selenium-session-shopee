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

BASE_SESSION = "H://Bot/bot lain/session shopee/session/"

def login(username, password):
    chrome_options = Options()
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument("--no-sandbox");
    chrome_options.add_argument("--headless");
    # chrome_options.add_argument("start-maximized");
    chrome_options.add_argument("disable-infobars");
    chrome_options.add_argument("--disable-extensions");
    chrome_options.add_argument("--disable-gpu");
    chrome_options.add_argument("--disable-dev-shm-usage");
    try:
        chrome_options.add_argument("--user-data-dir="+BASE_SESSION+username)
    except:
        hashInt = randint(1, 100)
        chrome_options.add_argument("--user-data-dir="+BASE_SESSION+username+hashInt)
			
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
        driver.find_element_by_xpath('//*[@class="navbar__username"]')
        print("[ INFO ]__main__: Logged in "+username)
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
def add_session():
    account = open('akun.txt')
    accounts = account.readlines()
    lengthAccount = len(accounts)+1

    for (akun, i) in zip(accounts, range(0, lengthAccount)):
        print(f"[ INFO ]__main__: in progress {i+1}/{lengthAccount}")
        accountStrip = akun.strip()
        username = accountStrip.split("|")[0]
        password = accountStrip.split("|")[1]
        login(username, password)

def read_session(username):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox");
    chrome_options.add_argument("start-maximized");
    chrome_options.add_argument("disable-infobars");
    chrome_options.add_argument("--disable-extensions");
    chrome_options.add_argument("--disable-gpu");
    chrome_options.add_argument("--disable-dev-shm-usage");
    chrome_options.add_argument("--user-data-dir="+BASE_SESSION+username)
			
    PATH = 'data/chromedriver'
    driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
    driver.get("https://shopee.co.id/")
	
    time = 1
    try:
        while True:
            os.system("cls")
            print("[ INFO ]_main_: session time "+ str(time))
            print("[ INFO ]_main_: ctrl + c to exit ")
            sleep(1)
            time+=1
        driver.quit()
    except:
        pass
	

def main():
    options = int(input("1. Create New Session\n2. Read Session\nChose options : "))
    if options == 1:
        add_session()
    elif options == 2:
        os.system("cls")
        username = input("Masukkan Username : ")
        read_session(username)

if __name__ == '__main__':
    try:
        os.mkdir("session")
    except:
        pass

    main()