from imap_reader import ImapClient
import json
from pathlib import Path

auth_file = Path(__file__).parent / "auth.json"

def getLogin():
    with open(auth_file, "a+", encoding="utf-8") as f:
        f.seek(0)
        content = f.read().strip()

        if not content:
            auth = {
                "email": input("Email to use for IMAP: "),
                "password": input("Password to use for IMAP: ")
            }
            f.seek(0)
            f.truncate()
            json.dump(auth, f, indent=2)
            return auth

        f.seek(0)
        return json.load(f)

def init():
    global auth
    auth = getLogin()

def getLatestEmail():
    with ImapClient(
            email_address=auth["email"],
            password_email=auth["password"],
        ) as client:
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