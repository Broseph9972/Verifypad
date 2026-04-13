from imap_reader import ImapClient
import json
from pathlib import Path
from datetime import datetime, timezone

def init(auth):
    global client
    client = ImapClient(
            email_address=auth["email"],
            password_email=auth["password"],
    )

def recievedWithinTime(date_str, seconds=30):
    """Return True if `date_str` occurred within the last `seconds` seconds."""
    try:
        message_time = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
    except (TypeError, ValueError):
        return False

    now = datetime.now(timezone.utc)
    elapsed = (now - message_time.astimezone(timezone.utc)).total_seconds()
    return 0 <= elapsed <= seconds

def getLatestEmail():
    msg = client.get_latest_message("UNSEEN")
    if msg:
        return msg
    else:
        return None

def getLatestOTP():
    email = getLatestEmail()
    if email and recievedWithinTime(email.date):
        return email.otp_codes

def getLatestLink():
    email = getLatestEmail()
    if email and recievedWithinTime(email.date):
        return email.verification_links