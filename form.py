import json

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

def get_child_info(child_number):
    print(f"\n--- Child {child_number} Information ---")
    child = {}
    child["Name"] = get_required("Child Name (First Last): ")
    child["Gender"] = get_required("Gender (Male/Female): ")
    child["Date of Birth"] = get_required("Date of Birth (YYYY-MM-DD): ")
    child["Age"] = get_required("Age: ")
    child["Allergies"] = input("Allergies (leave blank if none): ")
    return child

def main():
    print("WEIC Sunday School Registration Form 2025-26\n")

    form = {}

    # Primary child
    form["Children"] = []
    form["Children"].append(get_child_info(1))

    # Optional children
    for i in range(2, 4):
        add = get_yes_no(f"Do you want to add Child {i}?")
        if add == "Yes":
            form["Children"].append(get_child_info(i))
        else:
            break

    # Parent info
    print("\n--- Parent Information ---")
    form["Father's Name"] = get_required("Father's Name: ")
    form["Mother's Name"] = get_required("Mother's Name: ")
    form["Mailing Address"] = get_required("Mailing Address: ")
    form["Email Address 1"] = get_required("Email Address: ")
    form["Email Address 2"] = input("Secondary Email (optional): ")
    form["Father's Phone"] = get_required("Father's Phone Number: ")
    form["Mother's Phone"] = get_required("Mother's Phone Number: ")

    # Emergency contacts
    print("\n--- Emergency Contacts ---")
    form["Emergency Contact 1 Name"] = get_required("Emergency Contact 1 Name: ")
    form["Emergency Contact 1 Phone"] = get_required("Emergency Contact 1 Phone: ")
    form["Emergency Contact 2 Name"] = get_required("Emergency Contact 2 Name: ")
    form["Emergency Contact 2 Phone"] = get_required("Emergency Contact 2 Phone: ")

    # Permissions
    print("\n--- Permissions & Agreements ---")
    form["Photo/Video Consent"] = get_yes_no("Do you agree to photo/video usage?")
    form["Pickup Authorization"] = get_yes_no("Do you authorize pickup by listed contacts?")
    form["Liability Release"] = get_yes_no("Do you agree to the liability release?")

    form["Electronic Signature"] = get_required("Electronic Signature (Parent/Guardian Full Name): ")

    form["Scholarship Requested"] = get_yes_no("Do you require scholarship assistance?")

    # Save to file
    with open("registration.json", "w") as file:
        json.dump(form, file, indent=4)

    print("\n✅ Registration completed successfully!")
    print("Data saved to registration.json")

if __name__ == "__main__":
    main()
