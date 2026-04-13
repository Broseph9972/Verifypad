import config
import serialcomunication
import emailgetter
import paste
import time

serialOpen = False
configDict = {}

def messageHandler(msg):
    msg = msg.strip()
    if msg == "paste-otp":
        retry = 0
        while True:
            retry = retry + 1
            if retry > 5:
                serialcomunication.sendMessage("otp-paste-failed")
                break;
            codes = emailgetter.getLatestOTP()
            if codes:
                try:
                    paste.pasteText(codes[0])
                    serialcomunication.sendMessage("pasted-otp")
                except Exception:
                    serialcomunication.sendMessage("otp-paste-failed")
                break;
            time.sleep(3)
    elif msg == "paste-link":
        retry = 0
        while True:
            retry = retry + 1
            if retry > 4:
                serialcomunication.sendMessage("link-paste-failed")
                break;
            links = emailgetter.getLatestLink()
            if links:
                try:
                    paste.pasteText(links[0])
                    serialcomunication.sendMessage("pasted-link")
                except Exception:
                    serialcomunication.sendMessage("link-paste-failed")
                break;
            time.sleep(3)

def closeHandler():
    global serialOpen
    serialOpen = False
    print("Serial Connection lost. Attempting to establish a new connection.")
    WaitForSerialConnection()
    serialcomunication.start_monitoring()

def WaitForSerialConnection():
    global serialOpen
    tryAgainWait = 5
    while not serialcomunication.init(configDict["port"], messageHandler, closeHandler, True):
        print(f"Failed to start a serial connection. Will try again in {tryAgainWait}s.")
        time.sleep(tryAgainWait)
        tryAgainWait = tryAgainWait * 2
        if tryAgainWait > 60: tryAgainWait = 60
    print("Serial Connection Established")
    serialOpen = True

def loadConfig():
    global configDict
    configDict = config.getConfig() if config.checkForConfig() else config.setConfig()
    print("Config Loaded")

def initializeEmailScraper():
    global configDict
    emailgetter.init(configDict)
    print("Email Scraper Initialized")

def main():
    loadConfig()
    initializeEmailScraper()
    WaitForSerialConnection()
    serialcomunication.start_monitoring()

main()