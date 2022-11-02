import time
start_time = time.time()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Open Browser
option = webdriver.ChromeOptions()
option.add_argument("-incognito")
option.add_experimental_option("excludeSwitches", ['enable-logging'])
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

# Open File
line = open("isian.txt", "r").read().splitlines()
browser.get(line[0])
title = line[1]

# Get Element
dropdownClicks = browser.find_elements(By.CLASS_NAME, 'ry3kXd')
dropdownClicksIndex = 0
nextButton = browser.find_element(By.CLASS_NAME, 'lRwqcd').find_elements(By.CLASS_NAME, 'uArJ5e')[-1]

def fillform(isian):
    global dropdownClicksIndex, questions, questionIndex
    if len(isian.split("=")) == 2:
        tipe, isi = isian.split("=")
        question = questions[questionIndex]
        wait = WebDriverWait(question, 2)
        if tipe=="Email":
            browser.find_element(By.XPATH, "//input[@type = 'email']").send_keys(isi)
            print("Column 'Text' successfully filled with '{}'".format(isi))
            questionIndex -= 1
        elif tipe=="Text":
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "whsOnd")))
            question.find_element(By.CLASS_NAME, "whsOnd").send_keys(isi)
            print("Column 'Text' successfully filled with '{}'".format(isi))
        elif tipe=="Longtext":
            question.find_element(By.CSS_SELECTOR, "textarea").send_keys(isi)
            print("Column 'Long Text' successfully filled with '{}'".format(isi))
        elif tipe=="Multiple":
            #question.find_elements(By.CLASS_NAME, 'docssharedWizToggleLabeledContainer')[int(next(line))-1].click()
            question.find_element(By.XPATH, "//span[contains(text(),'{}')]".format(isi)).click()
            print("Column 'Multiple choice' successfully filled with '{}'".format(isi))
        elif tipe=="Checklist":
            for i,j in enumerate(isi.split(",")):
                for i in question.find_elements(By.XPATH, "//span[contains(text(),'{}')]".format(j)):
                    try:
                        i.click()
                    except Exception as e:
                        print(e)
            print("Column 'Checklist' successfully filled with '{}'".format(isi))
        elif tipe=="Dropdown":
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ry3kXd')))
            dropdownClicks[dropdownClicksIndex].click()
            time.sleep(0.7)
            for i in question.find_elements(By.XPATH, "//span[contains(text(),'{}')]".format(isi)):
                try:
                    i.click()
                except Exception as e:
                    print("", end="")
            dropdownClicksIndex += 1
            print("Column 'Dropdown' successfully filled with '{}'".format(isi))
            time.sleep(0.8)
        elif tipe=="Scale":
            question.find_elements(By.CLASS_NAME, 'T5pZmf')[int(isi)-1].click()
            print("Column 'Scale' successfully filled with '{}'".format(isi))
        elif tipe=="Date":
            question.find_element(By.XPATH, "//input[@type='date']").send_keys(isi)
            print("Column 'Date' successfully filled with '{}'".format(isi))
        elif tipe=="Time":
            times = isi.split(":")
            timesField = question.find_elements(By.CLASS_NAME, "whsOnd")
            timesField[0].send_keys(times[0])
            timesField[1].send_keys(times[1])
            print("Column 'Time' successfully filled with '{}'".format(isi))
        questionIndex += 1
    else:
        nextButton.click()
        print("\nGo to next section...\n")
        time.sleep(1)
        questions = browser.find_elements(By.CLASS_NAME, 'Qr7Oae')
        questions.pop(0)
        questionIndex = 0

# Get Question elements
questions = browser.find_elements(By.CLASS_NAME, "Qr7Oae")
questionIndex = 0

# Filling Form
WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'{}')]".format(title))))
for isian in line[2:]:
    fillform(isian)

# Submit Form
print("Press Enter to Submit", end="")
if input() == "":
    submitButton = browser.find_element(By.CLASS_NAME, 'lRwqcd').find_elements(By.CLASS_NAME, 'uArJ5e')
    submitButton[-1].click()
    print("Waktu Submit {} detik\n".format(time.time() - start_time))

# Wait till program close
t=10
while t>=0:
    mins, secs = divmod(t, 60)
    timer = 'Successfully submit your form. Browser will close in {:02d}:{:02d}'.format(mins, secs)
    print(timer, end="\r")
    time.sleep(1)
    t -= 1
time.sleep(0.2)
print("\n\nThankyou!\nYou can close this program")
browser.close()