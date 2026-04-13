from imap_reader import ImapClient
import json
from pathlib import Path

auth_file = Path(__file__).parent / "config.json"

def getLogin():
    with open(auth_file, "r", encoding="utf-8") as f:
        return json.load(f)

def init():
    global client
    auth = getLogin()
    client = ImapClient(
            email_address=auth["email"],
            password_email=auth["password"],
    )

def getLatestEmail():
    msg = client.get_latest_message("UNSEEN")
    if msg:
        return msg
    else:
        return None
        
def getLatestLink():
    email = getLatestEmail()
    if email:
        return email.otp_codes

def getLatestLink():
    email = getLatestEmail()
    if email:
        return email.verification_links