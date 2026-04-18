import config
import serialcomunication
import emailgetter
import paste
import time
import sys
import subprocess
import os
import art

serialOpen = False
configDict = {}

def messageHandler(msg):
    if msg == "paste-otp":
        print("Attempting to paste an OTP...")
        retry = 1
        while True:
            codes = emailgetter.getLatestOTP()
            if codes:
                paste.pasteText(codes[0])
                serialcomunication.sendMessage("pasted-otp")
                print("OTP Succesfully pasted: " + codes[0])
                break;
            print(f"Attemp {retry} of 5 failed. Will retry in 3 seconds.")
            retry = retry + 1
            if retry > 5:
                break;
            time.sleep(3)
        print("Reached maximum amount of attempts. Cancelling the paste attempt.")
        serialcomunication.sendMessage("otp-paste-failed")
    elif msg == "paste-link":
        print("Attempting to paste a link...")
        retry = 0
        while True:
            retry = retry + 1
            if retry > 4:
                break;
            links = emailgetter.getLatestLink()
            if links:
                paste.pasteText(links[0])
                serialcomunication.sendMessage("pasted-link")
                print("OTP Succesfully pasted: " + links[0])
                break;
            print(f"Attemp {retry} of 5 failed. Will retry in 3 seconds.")
            time.sleep(3)
            print("Reached maximum amount of attempts. Cancelling the paste attempt.")
        serialcomunication.sendMessage("link-paste-failed")

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

def attemptRestartInBackground():
    if "--background" in sys.argv:
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller EXE
            cmd = [sys.executable]
        else:
            # Running as .py script
            cmd = [sys.executable, os.path.abspath(__file__)]

        subprocess.Popen(
            cmd,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        print("Program has been re-launched in the background. Exiting.")
        sys.exit()
    print("Failed to re-launch in background, program will continue running normally.")

def main():
    #Command Line Arguments
    if len(sys.argv) > 1 and sys.argv[1] == "help":
        print("""
            VerifyPad Help:

            verifypad                   Run VerifyPad
            verifypad config            Configure VerifyPad program
            verifypad setport <port>    Set the COM port used by VerifyPad to communicate with the microcontroller
""")
        sys.exit()
    if len(sys.argv) > 1 and sys.argv[1] == "config":
        config.setConfig()
        print("Config has been updated.")
        sys.exit()
    if len(sys.argv) > 1 and sys.argv[1] == "setport":
        if(len(sys.argv) != 3):
            print("Please use the correct format: ...setport <port>")
            sys.exit()
        config.setPort(sys.argv[2])
        print("Config has been updated.")
        sys.exit()

    print(art.text2art("VerifyPad"))
    
    loadConfig()
    attemptRestartInBackground()
    initializeEmailScraper()
    WaitForSerialConnection()
    serialcomunication.start_monitoring()

if __name__ == "__main__":
    main()