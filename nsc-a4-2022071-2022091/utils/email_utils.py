# File: email_utils.py
import smtplib
from email.mime.text import MIMEText

# ─── CONFIGURE THESE ────────────────────────────────────────────────────────
SENDER_EMAIL    = "arav22091@iiitd.ac.in"         # your sender Gmail
SENDER_PASSWORD = "rkpu gzzq nmig edke"                   # your 16‑char App Password
# ──────────────────────────────────────────────────────────────────────────

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT   = 587

def send_otp_email(recipient: str, otp: str):
    """
    Sends an OTP via SMTP using configured sender credentials.
    """
    subject = "Your One‑Time Password"
    body    = f"Your OTP code is: {otp}\nPlease do not share it."
    msg     = MIMEText(body)
    msg["Subject"] = subject
    msg["From"]    = SENDER_EMAIL
    msg["To"]      = recipient

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)