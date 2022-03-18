from selenium import webdriver
import os
from selenium.webdriver.chrome.options import Options
from time import sleep
from tkinter import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


window = Tk()
window.title("WBulk")
window.resizable(False, False)
window.geometry("350x250")

programPath = os.path.dirname(os.path.realpath(__file__))

chrome_options = Options()
chrome_options.add_argument('log-level=3')
chrome_options.add_argument("user-data-dir=%s\\ChromeProfile" % programPath)
driver = webdriver.Chrome(executable_path="%s\\chromedriver.exe" % programPath, chrome_options=chrome_options)


with open("%s\\wbulk.config" % programPath, "r") as configFile:
  for line in configFile:
    if line.split("=")[0] == "runTimes":
      runTimes = line.split("runTimes=")[1].rstrip()
    elif line.split("=")[0] == "delay":
      delay = line.split("delay=")[1].rstrip()
configFile.close()


def sendMessage(times, target):
  i = 1
  try:
    targetButton = driver.find_elements_by_xpath("//*[contains(text(), '%s')]" % target)
    targetButton[0].click()

    while i <= times:
      try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')))
        driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]').send_keys("Te iubesc :heart" + Keys.RETURN)
        driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button').click()
      except Exception as ee:
        print(ee)
      i = i + 1
      sleep(int(delay))
    print("Job completed. Sent %s messages to %s" % (times, target))
  except Exception as e:
    print(e)

  driver.quit()
  exit()


def start():

  driver.get("https://web.whatsapp.com/")

  target = targetInput.get()

  window.destroy()

  try:
    driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[1]/div')
    print("WBulk -> Please log in.")
  except NoSuchElementException:
    try:
      WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div')))
      #driver.find_element_by_xpath('//*[@id="side"]/div[1]/div')
      print("Login correct! Good job.")
      sendMessage(int(runTimes), target)
    except Exception as e:
      print("Error 2: %s" % e)
  except Exception as e:
    print("Error 1: %s" % e)
  
  driver.quit()
  exit()


titleLabel = Label(window, text="WBulk", font=(None, 35))
titleLabel.pack(anchor=N, pady=(15, 0))

descriptionLabel = Label(window, text="Send SPAM WhatsApp messages!", font=(None, 10))
descriptionLabel.pack(anchor=NE, pady=(2, 30))

gridBox = Frame(window)
gridBox.pack(side=TOP)

targetLabel = Label(gridBox, text="Target")
targetLabel.grid(column=0, row=0, padx=(0, 3))

targetInput = Entry(gridBox, width=20)
targetInput.grid(row=0, column=1)

spamButton = Button(window, text="SPAM", command=lambda:start())
spamButton.pack(pady=(10, 0))

window.mainloop()