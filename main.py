from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import os
import schedule
import datetime

running = True # This variable will be used to stop program

def login():
    credentials = []
    for word in open('credentials.txt','r'):
        temp = [i.strip() for i in word.split('=')]
        credentials.append(temp[1])

    # email details and submit button click
    elem = driver.find_element_by_id('i0116').send_keys(f'{credentials[0]}')
    driver.implicitly_wait(3)
    elem = driver.find_element_by_id('idSIButton9').click()
    driver.implicitly_wait(10)
    time.sleep(10)

    # password details and submit button click
    elem = driver.find_element_by_id('i0118').send_keys(f'{credentials[1]}')
    time.sleep(5)
    elem = driver.find_element_by_id('idSIButton9').click()
    driver.implicitly_wait(5)

    # stay signed in page
    elem = driver.find_element_by_id('idSIButton9').click()
    time.sleep(5)

    # use web app instead page
    elem = driver.find_element_by_link_text('Use the web app instead').click()
    time.sleep(20)

def class_join(sub_name):
    while True:
        try:
            try:
                # Team we want to join
                elem = driver.find_element_by_xpath(f'//*[@title="{sub_name}"]').click()
                time.sleep(15)
            except NoSuchElementException:
                print(f"Couldn't find class named: {sub_name}, please edit your file.")
                time.sleep(7)
                quit()

            # Join button in that team
            elem = driver.find_element_by_xpath('//*[@aria-label="Join"]').click()
            time.sleep(15)

            # Muting microphone if not muted
            try:
                elem = driver.find_element_by_xpath('//*[@title="Mute microphone"]').click()
                time.sleep(1)
            except NoSuchElementException:
                pass

            # Turning off camera if not not turned off
            try:
                elem = driver.find_element_by_xpath('//*[@title="Turn camera off"]').click()
            except NoSuchElementException:
                pass

            # Join button in overlay
            elem = driver.find_element_by_xpath('//*[@aria-label="Join the meeting"]').click()
            print(f"{sub_name} Joined")
            time.sleep(12)
            break

        except NoSuchElementException:
            driver.refresh()
            time.sleep(60)

def end_call(sub_name):
    # End call button
    try:
        elem = driver.find_element_by_id('hangup-button')
        driver.execute_script("$(arguments[0]).click();", elem)
        print(f"{sub_name} ended")
        time.sleep(3)
        try:
            elem = driver.find_element_by_xpath('//*[@aria-label="Dismiss"]').click()
        except:
            pass
    except NoSuchElementException:
        print("Class already ended or didn't start")
        pass

def exit_bot():
    global running
    running = False

while True:
    try:
        # Bypassing mic and video permissions
        options = Options()
        options.add_argument("--use-fake-ui-for-media-stream")

        # open chrome
        driver = webdriver.Chrome(options=options)

        # Maximize window
        driver.maximize_window()

        # website open
        driver.get('https://go.microsoft.com/fwlink/p/?LinkID=873020&culture=en-us&country=WW&lm=deeplink&lmsrc=homePageWeb&cmpid=WebSignIn/')
        driver.implicitly_wait(10)
        login()
        break
    except:
        driver.quit()

# Retrieving data from text file
today = datetime.datetime.now().strftime("%A")
list = []
for word in open(f'{today}.txt','r'):
    temp = [i.strip() for i in word.split('=')]
    list.append(temp[1])

# Scheduling classes.
i = 0
while i < len(list):
    schedule.every().day.at(f"{list[i+1]}").do(class_join, sub_name = f"{list[i]}")
    schedule.every().day.at(f"{list[i+2]}").do(end_call, sub_name = f"{list[i]}")
    if i == len(list)-3:
        schedule.every().day.at(f"{list[i+2]}").do(exit_bot)
    i+=3

# schedule loop to keep it running.
while running:
    schedule.run_pending()
    time.sleep(1)
