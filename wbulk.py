from selenium import webdriver
import os
from selenium.webdriver.chrome.options import Options
from time import sleep
from tkinter import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from tkinter import messagebox


### Tkinter window ###
window = Tk()
window.title("WBulk")
window.resizable(False, False)
window.geometry("350x300")

### Program Path ###
programPath = os.path.dirname(os.path.realpath(__file__))

### Chrome Options ###
chrome_options = Options()
chrome_options.add_argument('log-level=3')
chrome_options.add_argument("user-data-dir=%s\\ChromeProfile" % programPath)

### DRIVER ###
driver = webdriver.Chrome(executable_path="%s\\chromedriver.exe" % programPath, chrome_options=chrome_options)

### Icons ###
spamButtonIcon = PhotoImage(file="%s\\icons\\ok.png" % programPath)
cautionButtonIcon = PhotoImage(file="%s\\icons\\caution.png" % programPath)
backButtonIcon = PhotoImage(file="%s\\icons\\back.png" % programPath)

### WBulk config file ###
with open("%s\\wbulk.config" % programPath, "r") as configFile:
  for line in configFile:
    if line.split("=")[0] == "runTimes":
      runTimes = line.split("runTimes=")[1].rstrip()
    elif line.split("=")[0] == "delay":
      delay = line.split("delay=")[1].rstrip()
    elif line.split("=")[0] == "payload":
      payload = line.split("payload=")[1].rstrip()
configFile.close()


def cautionPage():
  for widget in window.winfo_children():
    widget.destroy()
  disclaimerLabel = Label(window, text="I am not responsible for the damage caused by this program. Use this program with responsibility!", wraplength=300, font=(None, 20))
  disclaimerLabel.pack()
  backButton = Button(window, image=backButtonIcon, border="0", command=lambda:init())
  backButton.pack(anchor=S, side=LEFT)


# Show the buttons and text on the screen 
def init():
  for widget in window.winfo_children():
    widget.destroy()
  titleLabel = Label(window, text="WBulk", font=(None, 35))
  titleLabel.pack(anchor=N, pady=(15, 0))

  descriptionLabel = Label(window, text="Send SPAM WhatsApp messages!", font=(None, 10))
  descriptionLabel.pack(anchor=N, pady=(2, 30))

  gridBox = Frame(window)
  gridBox.pack(side=TOP)

  targetLabel = Label(gridBox, text="Target")
  targetLabel.grid(column=0, row=0, padx=(0, 3))

  targetInput = Entry(gridBox, width=20)
  targetInput.grid(row=0, column=1)

  spamButton = Button(window, command=lambda:start(targetInput.get()), border="0", image=spamButtonIcon)
  spamButton.pack(side=RIGHT, anchor=SE)

  cautionButton = Button(window, border="0", image=cautionButtonIcon, command=lambda:cautionPage())
  cautionButton.pack(side=LEFT, anchor=SE)

  window.mainloop()


def sendMessage(times, target):
  i = 1
  try:
    # Search the target
    targetButton = driver.find_elements_by_xpath("//*[contains(text(), '%s')]" % target)
    # Click the target to open the chat
    targetButton[0].click()

    while i <= times:
      try:
        # Wait until the message box is successfully loaded
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')))
        # Write the message to target
        driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]').send_keys(payload)
        # Send the messafe
        driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button').click()
      except Exception as e:
        print("Error 4: %s" % e)
      i = i + 1
      # Wait an amount of time
      sleep(int(delay))
    print("Job completed. Sent %s messages to %s" % (times, target))
    messagebox.showinfo("Job completed", "Job completed. Sent %s messages to %s" % (times, target))
  except Exception as e:
    print("Error 3: %s" % e)


def login(targetInput):
  try:
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div'))) # Check of the browser confirms the login
    print("Login correct! Good job.")
    # Send messages script
    sendMessage(int(runTimes), targetInput)
  except Exception as e:
    print("Error 2: %s" % e)


def start(targetInput):
  if targetInput == "":
    init()
  else:
    question = messagebox.askquestion("SPAM %s?", "Are you sure you want to send %s messages to %s? Make a responsable decision!" % (int(runTimes), targetInput), icon='warning')
    if question == "yes":
      window.destroy()
      driver.get("https://web.whatsapp.com/")

      # Check if the user is logged in 
      try:
        driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[1]/div')
        print("WBulk -> Please log in.")
        login(targetInput)
      except NoSuchElementException:
        login(targetInput)
      except Exception as e:
        print("Error 1: %s" % e)
    else:
      driver.quit()
      exit()

init()
# Exit when the last message is sent
driver.quit()
exit()