from imap_reader import ImapClient
import json

def getLogin():
    with open("auth.json", "a+", encoding="utf-8") as f:
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

def getLatestEmailBody():
    with ImapClient(
            email_address=auth["email"],
            password_email=auth["password"],
        ) as client:
        msg = client.get_latest_message("UNSEEN")
        if msg:
            return (True, msg.body_text)
        else:
            return (False, None)