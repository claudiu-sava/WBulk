# WBulk - WhatsApp Bulk Message Sender



# How to use
**Caution! This tool runs on Windows OS only!**

**!! While using WBulk Chrome will start automatically. Do not close it !!**

## How to start WBulk

In order for WBulk to run you need to have Chrome v99 installed. Check the chrome version by accessing this link inside Chrome browser: `chrome://settings/help`. 

If the verison differs, please [download the chromedriver](https://chromedriver.chromium.org/downloads) for your Chrome version and put it in the root of WBulk folder (overwriting the old chromedriver.exe file).

### Windows Executable (exe)

This is the easiest way to run WBulk. 

1. Download the [latest version](https://github.com/claudiu-sava/WBulk/releases/)
2. Unzip the files and run wbulk.exe

### Python Script (py)

**!! Before running the script make sure you have Python installed !!**

1. Install the requirements: `pip install -r requirements.txt` - **Python2 isn't accepted anymore**
2. Run the script: `python WBulk.py`

## How to configure WBulk

Open `wbulk.config` with your favourite text editor. 
 
 runTimes | delay | payload
 --- | --- | ---
How many messages do you want to send? | How many seconds pause between messages? (min 1s)| What is your message?

Simply change the values, close the file and start WBulk to run the new settings.

**!! Don't put any space between `=` and the value !!**

# CAUTION

Do not expose the `ChromeProfile` folder to nobody! It may contain sensitive data! 
