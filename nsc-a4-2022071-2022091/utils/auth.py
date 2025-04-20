# File: auth.py
import getpass
import random
import bcrypt
from db import users_collection
from ntp_time import get_gmt_datetime
from email_utils import send_otp_email

OTP_EXPIRY_MINUTES = 5

def signup():
    print("=== Signup ===")
    name = input("Full Name: ").strip()
    roll_number = input("Roll Number: ").strip()
    email = input("Email (Gmail): ").strip()
    if not email.endswith("@iiitd.ac.in"):
        print("Error: Email must be a IIITD address.")
        return False
    # Generate and send OTP
    otp = str(random.randint(100000, 999999))
    send_otp_email(email, otp)
    user_otp = input("Enter the OTP sent to your email: ").strip()
    if user_otp != otp:
        print("Invalid OTP. Signup failed.")
        return False
    dob = input("Date of Birth (YYYY-MM-DD): ").strip()
    pincode = input("Home Pincode: ").strip()
    college = input("College Name: ").strip()
    grad_year = input("Year of Graduation: ").strip()
    password = getpass.getpass("Password: ")
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    if users_collection.find_one({"roll_number": roll_number}):
        print("User with this roll number already exists.")
        return False
    users_collection.insert_one({
        "name": name,
        "roll_number": roll_number,
        "email": email,
        "dob": dob,
        "pincode": pincode,
        "college": college,
        "grad_year": grad_year,
        "password_hash": password_hash
    })
    print("Signup successful.")
    return True

def login():
    print("=== Login ===")
    roll_number = input("Roll Number: ").strip()
    password = getpass.getpass("Password: ")
    user = users_collection.find_one({"roll_number": roll_number})
    if not user or not bcrypt.checkpw(password.encode(), user["password_hash"]):
        print("Invalid credentials.")
        return None
    # Two-factor via email
    otp = str(random.randint(100000, 999999))
    send_otp_email(user["email"], otp)
    user_otp = input("Enter the OTP sent to your email: ").strip()
    if user_otp != otp:
        print("Invalid OTP. Login failed.")
        return None
    login_time = get_gmt_datetime()
    print("Login successful.")
    user["login_time"] = login_time
    return user

