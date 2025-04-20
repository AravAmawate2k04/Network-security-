#!/usr/bin/env python3
import sys
import json
from auth import signup_cli, login_cli
from db import users_collection
from pdf_generator import generate_degree_certificate, generate_grade_report

def main():
    data   = json.load(sys.stdin)
    action = data.get("action")

    if action == "signup":
        # { action, name, roll_number, dob, pincode, email, college, grad_year, password[, otp] }
        res = signup_cli(data)
        print(json.dumps(res))
        return

    if action == "login":
        # { action, roll_number, password[, otp] }
        res = login_cli(data)
        print(json.dumps(res))
        return

    if action == "generate":
        # { action, roll_number }
        roll = data.get("roll_number")
        if not roll:
            print(json.dumps({"error": "Missing field roll_number"}))
            return

        # fetch user who has logged in (login_time must exist)
        user_doc = users_collection.find_one({
            "roll_number": roll,
            "login_time": {"$exists": True}
        })
        if not user_doc:
            print(json.dumps({"error": "User not logged in or session expired"}))
            return

        # build a sanitized user dict for PDF generation
        user = {
            "name":        user_doc["name"],
            "roll_number": user_doc["roll_number"],
            "dob":         user_doc["dob"],
            "pincode":     user_doc["pincode"],
            "email":       user_doc["email"],
            "college":     user_doc["college"],
            "grad_year":   user_doc["grad_year"],
            "login_time":  user_doc["login_time"]
        }

        # generate both PDFs
        degree_path = generate_degree_certificate(user)
        grade_path  = generate_grade_report(user)

        print(json.dumps({
            "degree_path": degree_path,
            "grade_path":  grade_path
        }))
        return

    # unknown action
    print(json.dumps({"error": f"Unknown action: {action}"}))


if __name__ == "__main__":
    main()
