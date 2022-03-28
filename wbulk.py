from lib2to3.pgen2 import driver
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

### Program Path ###
programPath = os.path.dirname(os.path.realpath(__file__))

### Tkinter window ###
window = Tk()
window.title("WBulk")
window.resizable(False, False)
window.geometry("350x450")
window.iconbitmap("%s\\icons\\wbulk.ico" % programPath)

### Chrome Options ###
chrome_options = Options()
chrome_options.add_argument('log-level=3')
chrome_options.add_argument("user-data-dir=%s\\ChromeProfile" % programPath)

### Icons ###
spamButtonIcon = PhotoImage(file="%s\\icons\\ok.png" % programPath)
cautionButtonIcon = PhotoImage(file="%s\\icons\\caution.png" % programPath)
backButtonIcon = PhotoImage(file="%s\\icons\\back.png" % programPath)


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
  descriptionLabel.pack(anchor=N, pady=(2, 0))


  gridBox = Frame(window)
  gridBox.pack(side=TOP, pady=(30, 0))

  targetLabel = Label(gridBox, text="Target")
  targetLabel.grid(column=0, row=0, padx=(0, 3))

  targetInput = Entry(gridBox, width=20)
  targetInput.grid(row=0, column=1)

  messageNumberLabel = Label(gridBox, text="Number of messages")
  messageNumberLabel.grid(row=1, column=0, padx=(0, 3), pady=(5, 0))

  messageNumberInput = Entry(gridBox, width=20)
  messageNumberInput.grid(row=1, column=1)

  delayLabel = Label(gridBox, text="Delay")
  delayLabel.grid(row=2, column=0, padx=(0, 3), pady=(3, 0))

  delayInput = Entry(gridBox, width=20)
  delayInput.grid(row=2, column=1)

  payloadLabel = Label(window, text="Payload")
  payloadLabel.pack(pady=(10, 0))

  payloadText = Text(window, height = 5, width = 35)
  payloadText.pack(pady=(5, 0))

  spamButton = Button(window, command=lambda:start(targetInput.get(), messageNumberInput.get(), payloadText.get("1.0","end-1c"), delayInput.get()), border="0", image=spamButtonIcon)
  spamButton.pack(side=RIGHT, anchor=SE)

  cautionButton = Button(window, border="0", image=cautionButtonIcon, command=lambda:cautionPage())
  cautionButton.pack(side=LEFT, anchor=SE)

  window.mainloop()


def sendMessage(datas, driver):
  i = 1
  try:
    try:
      # Search the target
      targetButton = driver.find_elements_by_xpath("//*[contains(text(), '%s')]" % datas[0])

      # Click the target to open the chat
      targetButton[0].click()
    except Exception as e:
      print("Error 5: Details: %s" % e)

    while i <= int(datas[1]):
      try:
        # Wait until the message box is successfully loaded
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]')))
        # Write the message to target
        driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]').send_keys(datas[2])
        # Send the messafe
        driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button').click()
      except Exception as e:
        print("Error 4: %s" % e)
        messagebox.showerror("Error 4", "Error 4 occurred. Details: %s" % e)
      i = i + 1
      # Wait an amount of time
      sleep(int(datas[3]))
    print("Job completed. Sent %s messages to %s" % (datas[1], datas[0]))
    messagebox.showinfo("Job completed", "Job completed. Sent %s messages to %s" % (datas[1], datas[0]))

    # Exit when the last message is sent
    driver.quit()
    exit()
  except Exception as e:
    print("Error 3: %s" % e)
    messagebox.showerror("Error 3", "Error 3 occurred. Details: %s" % e)


def login(datas, driver):
  try:
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div'))) # Check of the browser confirms the login
    print("Login correct! Good job.")
    # Send messages script
    sendMessage(datas, driver)
  except Exception as e:
    messagebox.showerror("Error 2", "Error 2 occurred. Details: %s" % e)
    print("Error 2: %s" % e)


def start(targetInput, messageNumberInput, payloadText, delayInput):
  if targetInput == "" or messageNumberInput == "" or payloadText == "" or delayInput == "":
    init()
  try:
    messageNumberInput = int(messageNumberInput)
    delayInput = int(delayInput)
  except:
    init()
  else:
    datas = [targetInput, messageNumberInput, payloadText, delayInput]
    question = messagebox.askquestion("SPAM %s?" % targetInput, "Are you sure you want to send %s messages to %s? Make a responsable decision!" % (messageNumberInput, targetInput), icon='warning')
    if question == "yes":
      ### DRIVER ###
      driver = webdriver.Chrome(executable_path="%s\\chromedriver.exe" % programPath, chrome_options=chrome_options)
      
      window.destroy()
      driver.get("https://web.whatsapp.com/")

      # Check if the user is logged in 
      try:
        driver.find_element_by_xpath('//*[@id="app"]/div[1]/div/div[1]/div')
        print("WBulk -> Please log in.")
        login(datas, driver)
      except NoSuchElementException:
        login(datas, driver)
      except Exception as e:
        print("Error 1: %s" % e)
        messagebox.showerror("Error 1", "Error 1 occurred. Details: %s" % e)

init()
