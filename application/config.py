import json
from pathlib import Path

auth_file = Path(__file__).parent / "config.json"

def checkForConfig():
    try:
        with open(auth_file, "r", encoding="utf-8") as f:
            config = json.load(f)
            if "email" in config and "password" in config and "port" in config:
                return True
            else:  
                return False
    except:
        return False

def getConfig():
    with open(auth_file, "r", encoding="utf-8") as f:
        return json.load(f)

def setConfig():
    with open(auth_file, "w", encoding="utf-8") as f:
        config = {
            "email": input(f"Email to use for IMAP: "),
            "password": input(f"Password to use for IMAP: "),
            "port": input(f"Serial Comunication Port to use: ")
        }
        json.dump(config, f, indent=2)
        return config
    
def setPort(port):
    config = getConfig()
    config["port"] = port
    with open(auth_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
        return config