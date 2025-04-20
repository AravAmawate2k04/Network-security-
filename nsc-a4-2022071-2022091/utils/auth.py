# File: utils/auth.py

from db import users_collection
from email_utils import send_otp_email
import random, datetime, bcrypt
from bson.objectid import ObjectId

# how long OTPs stay valid
OTP_TTL = datetime.timedelta(minutes=5)


def signup_cli(data):
    """
    data: {
      name, roll_number, dob, pincode,
      email, college, grad_year, password[, otp]
    }
    returns {"status":"otp_sent"} or {"status":"ok"} or {"error": "..."}
    """
    try:
        # 1) Validate required fields
        required = [
            "name","roll_number","dob",
            "pincode","email","college",
            "grad_year","password"
        ]
        for f in required:
            if f not in data or not data[f]:
                return {"error": f"Missing field {f}"}

        # 2) Check if user exists already
        existing = users_collection.find_one({"roll_number": data["roll_number"]})

        # If fully verified already, cannot signup again
        if existing and existing.get("verified"):
            return {"error": "User already exists"}

        # OTP flow
        if "otp" in data:
            if not existing:
                return {"error": "No signup in progress for this roll number"}
            # check OTP match & expiry
            if existing.get("otp") != data["otp"]:
                return {"error": "Invalid OTP"}
            if existing.get("otp_expiry") < datetime.datetime.utcnow():
                return {"error": "OTP expired"}
            # mark verified and remove OTP fields
            users_collection.update_one(
                {"_id": existing["_id"]},
                {
                    "$set": {"verified": True},
                    "$unset": {"otp": "", "otp_expiry": ""}
                }
            )
            return {"status": "ok"}

        # First step: generate OTP, hash password, store record
        otp    = f"{random.randint(0,999999):06d}"
        expiry = datetime.datetime.utcnow() + OTP_TTL

        # hash the password
        pwd_hash = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()

        if existing:
            # update the signup record (in case they re‑submitted)
            users_collection.update_one(
                {"_id": existing["_id"]},
                {"$set": {
                    "name": data["name"],
                    "dob": data["dob"],
                    "pincode": data["pincode"],
                    "email": data["email"],
                    "college": data["college"],
                    "grad_year": data["grad_year"],
                    "password_hash": pwd_hash,
                    "otp": otp,
                    "otp_expiry": expiry
                }}
            )
        else:
            # new signup
            users_collection.insert_one({
                "name":         data["name"],
                "roll_number":  data["roll_number"],
                "dob":          data["dob"],
                "pincode":      data["pincode"],
                "email":        data["email"],
                "college":      data["college"],
                "grad_year":    data["grad_year"],
                "password_hash":pwd_hash,
                "verified":     False,
                "otp":          otp,
                "otp_expiry":   expiry
            })

        # send OTP email
        send_otp_email(data["email"], otp)
        return {"status": "otp_sent"}

    except Exception as e:
        return {"error": str(e)}


def login_cli(data):
    """
    data: { roll_number, password[, otp] }
    returns {"status":"otp_sent"} or {"status":"ok","user":{…}} or {"error":"..."}
    """
    try:
        # 1) Validate fields
        if "roll_number" not in data or not data["roll_number"]:
            return {"error": "Missing roll_number"}
        if "password" not in data or not data["password"]:
            return {"error": "Missing password"}

        # 2) Lookup user (must be verified)
        user = users_collection.find_one({
            "roll_number": data["roll_number"],
            "verified":    True
        })
        if not user:
            return {"error": "Invalid roll number or user not verified"}

        # 3) Verify password
        if not bcrypt.checkpw(data["password"].encode(),
                              user["password_hash"].encode()):
            return {"error": "Invalid password"}

        # OTP step?
        if "otp" in data:
            # verify OTP
            if user.get("otp") != data["otp"]:
                return {"error": "Invalid OTP"}
            if user.get("otp_expiry") < datetime.datetime.utcnow():
                return {"error": "OTP expired"}

            # 4) Finalize login: stamp login_time, clear OTP
            login_time = datetime.datetime.utcnow()
            users_collection.update_one(
                {"_id": user["_id"]},
                {
                    "$set": {"login_time": login_time},
                    "$unset": {"otp": "", "otp_expiry": ""}
                }
            )

            # return sanitized user + login_time
            return {
                "status": "ok",
                "user": {
                    "name":        user["name"],
                    "roll_number": user["roll_number"],
                    "college":     user["college"],
                    "grad_year":   user["grad_year"],
                    "login_time":  login_time.isoformat()  # JSON‑serializable
                }
            }

        # First login step: generate + store OTP
        otp    = f"{random.randint(0,999999):06d}"
        expiry = datetime.datetime.utcnow() + OTP_TTL
        users_collection.update_one(
            {"_id": user["_id"]},
            {"$set": {"otp": otp, "otp_expiry": expiry}}
        )
        send_otp_email(user["email"], otp)
        return {"status": "otp_sent"}

    except Exception as e:
        return {"error": str(e)}
