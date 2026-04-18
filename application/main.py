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
    configDict = config.getConfig()
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

    content = tk.Frame(container, bg="#11131a")
    content.pack(fill="both", expand=True, padx=28, pady=22)

    status_label = tk.Label(
        content,
        text="",
        bg="#11131a",
        fg="#f3f6ff",
        anchor="w",
        justify="left",
        font=("JetBrains Mono", 10)
    )
    status_label.pack(fill="x")

    worker_started = {"value": False}

    def start_backend_worker():
        if worker_started["value"]:
            return
        worker_started["value"] = True
        status_label.config(text="Starting VerifyPad services...")
        worker = threading.Thread(
            target=lambda: (loadConfig(), initializeEmailScraper(), WaitForSerialConnection(), serialcomunication.start_monitoring()),
            daemon=True
        )
        worker.start()

    def add_labeled_entry(parent, label, is_password=False):
        row = tk.Frame(parent, bg="#11131a")
        row.pack(fill="x", pady=6)
        tk.Label(
            row,
            text=label,
            bg="#11131a",
            fg="#cfd6ef",
            font=("JetBrains Mono", 10)
        ).pack(anchor="w")
        entry = tk.Entry(
            row,
            bg="#1b2130",
            fg="#f3f6ff",
            insertbackground="#f3f6ff",
            relief="flat",
            font=("JetBrains Mono", 10),
            show="*" if is_password else ""
        )
        entry.pack(fill="x", ipady=7)
        return entry

    if not config.checkForConfig():
        status_label.config(text="Set up VerifyPad to continue.")

        form = tk.Frame(content, bg="#11131a")
        form.pack(fill="x", pady=(14, 0))

        email_entry = add_labeled_entry(form, "Email")
        password_entry = add_labeled_entry(form, "Password", is_password=True)
        port_entry = add_labeled_entry(form, "Serial Port (for example COM3)")

        def save_config_and_start():
            email = email_entry.get().strip()
            password = password_entry.get().strip()
            port = port_entry.get().strip()

            if not email or not password or not port:
                status_label.config(text="Please fill in Email, Password, and Serial Port.", fg="#ff8080")
                return

            config.setConfig({
                "email": email,
                "password": password,
                "port": port
            })
            status_label.config(text="Config saved. Starting services...", fg="#8ff0a4")
            save_button.config(state="disabled")
            email_entry.config(state="disabled")
            password_entry.config(state="disabled")
            port_entry.config(state="disabled")
            start_backend_worker()

        save_button = tk.Button(
            content,
            text="Save and Start",
            command=save_config_and_start,
            bg="#33415f",
            fg="#f3f6ff",
            activebackground="#42557c",
            activeforeground="#ffffff",
            relief="flat",
            bd=0,
            padx=18,
            pady=9,
            font=("JetBrains Mono", 10, "bold")
        )
        save_button.pack(anchor="w", pady=12)
    else:
        status_label.config(text="Config found. Starting VerifyPad services...")
        start_backend_worker()

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
        print("Use the desktop GUI to set Email, Password, and Serial Port.")
        sys.exit()
    if len(sys.argv) > 1 and sys.argv[1] == "setport":
        if(len(sys.argv) != 3):
            print("Please use the correct format: ...setport <port>")
            sys.exit()
        config.setPort(sys.argv[2])
        print("Config has been updated.")
        sys.exit()

    runGui()
    serialcomunication.closeConnection()

if __name__ == "__main__":
    main()