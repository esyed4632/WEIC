import json
import re
from datetime import datetime

def get_required(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field is required.")

def get_yes_no(prompt):
    while True:
        value = input(prompt + " (Yes/No): ").strip().lower()
        if value in ["yes", "no"]:
            return value.capitalize()
        print("Please enter Yes or No.")

def get_gender(prompt):
    while True:
        value = input(prompt + " (Male/Female): ").strip().lower()
        if value in ["male", "female"]:
            return value.capitalize()
        print("Please enter Male or Female.")

def get_age(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit() and int(value) > 0:
            return int(value)
        print("Age must be a positive number.")

def get_date(prompt):
    while True:
        value = input(prompt).strip()
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Date must be in YYYY-MM-DD format.")

def get_phone(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit() and 10 <= len(value) <= 15:
            return value
        print("Phone number must be 10–15 digits.")

def get_email(prompt, required=True):
    while True:
        value = input(prompt).strip()
        if not value and not required:
            return ""
        if re.match(r"^[^@]+@[^@]+\.[^@]+$", value):
            return value
        print("Please enter a valid email address.")

def get_child_info(child_number):
    print(f"\n--- Child {child_number} Information ---")
    child = {}
    child["Name"] = get_required("Child Name (First Last): ")
    child["Gender"] = get_gender("Gender")
    child["Date of Birth"] = get_date("Date of Birth (YYYY-MM-DD): ")
    child["Age"] = get_age("Age: ")
    child["Allergies"] = input("Allergies (leave blank if none): ").strip()
    return child

def main():
    print("WEIC Sunday School Registration Form 2025-26\n")

    form = {}

    form["Children"] = []
    form["Children"].append(get_child_info(1))

    for i in range(2, 4):
        add = get_yes_no(f"Do you want to add Child {i}?")
        if add == "Yes":
            form["Children"].append(get_child_info(i))
        else:
            break

    print("\n--- Parent Information ---")
    form["Father's Name"] = get_required("Father's Name: ")
    form["Mother's Name"] = get_required("Mother's Name: ")
    form["Mailing Address"] = get_required("Mailing Address: ")
    form["Email Address 1"] = get_email("Email Address: ")
    form["Email Address 2"] = get_email("Secondary Email (optional): ", required=False)
    form["Father's Phone"] = get_phone("Father's Phone Number: ")
    form["Mother's Phone"] = get_phone("Mother's Phone Number: ")

    print("\n--- Emergency Contacts ---")
    form["Emergency Contact 1 Name"] = get_required("Emergency Contact 1 Name: ")
    form["Emergency Contact 1 Phone"] = get_phone("Emergency Contact 1 Phone: ")
    form["Emergency Contact 2 Name"] = get_required("Emergency Contact 2 Name: ")
    form["Emergency Contact 2 Phone"] = get_phone("Emergency Contact 2 Phone: ")

    print("\n--- Permissions & Agreements ---")
    form["Photo/Video Consent"] = get_yes_no("Do you agree to photo/video usage?")
    form["Pickup Authorization"] = get_yes_no("Do you authorize pickup by listed contacts?")
    form["Liability Release"] = get_yes_no("Do you agree to the liability release?")
    form["Scholarship Requested"] = get_yes_no("Do you require scholarship assistance?")

    form["Electronic Signature"] = get_required(
        "Electronic Signature (Parent/Guardian Full Name): "
    )

    file = open("registration.json", "w")
    json.dump(form, file, indent=4)
    file.close()

    print("\n✅ Registration completed successfully!")
    print("Data saved to registration.json")

if __name__ == "__main__":
    main()
