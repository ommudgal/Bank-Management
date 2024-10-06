import smtplib
from dotenv import load_dotenv
import os

load_dotenv()


def send_otp(email, otp):
    sender_email = os.getenv("gmail")
    sender_password = os.getenv("gmail_key")
    message = f"Subject: OTP\n\nYour OTP is {otp}"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, email, message)
    server.quit()


def generate_otp():
    import random

    return random.randint(100000, 999999)
