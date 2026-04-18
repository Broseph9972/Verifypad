import config
import serialcomunication
import emailgetter
import paste
import time
import sys
import threading
import tkinter as tk
from pathlib import Path
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


def runGui():
    root = tk.Tk()
    root.title("VerifyPad")
    icon_path = Path(__file__).with_name("icon.ico")
    try:
        root.iconbitmap(default=str(icon_path))
    except tk.TclError:
        print(f"Failed to load window icon: {icon_path}")
    root.geometry("680x420")
    root.minsize(460, 280)
    root.configure(bg="#11131a")

    container = tk.Frame(root, bg="#11131a")
    container.pack(fill="both", expand=True)

    quit_button = tk.Button(
        container,
        text="Quit",
        command=root.destroy,
        bg="#1f2430",
        fg="#f3f6ff",
        activebackground="#2a3140",
        activeforeground="#ffffff",
        relief="flat",
        bd=0,
        padx=26,
        pady=10,
        font=("JetBrains Mono", 12, "bold")
    )
    quit_button.pack(side="bottom", pady=22)

    root.mainloop()

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

    
    worker = threading.Thread(
        target=lambda: (loadConfig(), initializeEmailScraper(), WaitForSerialConnection(), serialcomunication.start_monitoring()),
        daemon=True
    )
    worker.start()
    runGui()
    serialcomunication.closeConnection()

if __name__ == "__main__":
    main()