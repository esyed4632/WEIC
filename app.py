from flask import Flask, render_template, request, redirect, url_for, flash
import json
import re

app = Flask(__name__)
app.secret_key = "supersecretkey"  # needed for flash messages

# -------------------------
# Constants
# -------------------------
MIN_AGE = 5
MAX_AGE = 13

# -------------------------
# Validation functions
# -------------------------
def validate_email(email):
    if not email:  # secondary email can be empty
        return True
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_phone(phone):
    return re.match(r"^\d{10}$", phone)  # simple 10-digit check

# -------------------------
# Routes
# -------------------------
@app.route("/", methods=["GET"])
def form():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    # Get form data
    age_str = request.form.get("age")
    try:
        age = int(age_str)
    except (ValueError, TypeError):
        flash("Invalid age.")
        return redirect(url_for("form"))

    # Age restrictions
    if age < MIN_AGE:
        flash("Too young — cannot apply.")
        return redirect(url_for("form"))
    elif age > MAX_AGE:
        flash("Too old — registration closed.")
        return redirect(url_for("form"))

    # Build registration dict
    data = {
        "Child": {
            "Name": request.form.get("childName"),
            "Gender": request.form.get("gender"),
            "Date of Birth": request.form.get("dob"),
            "Age": age,
            "Allergies": request.form.get("allergies")
        },
        "Father's Name": request.form.get("fatherName"),
        "Mother's Name": request.form.get("motherName"),
        "Mailing Address": request.form.get("address"),
        "Email Address 1": request.form.get("email1"),
        "Email Address 2": request.form.get("email2"),
        "Father's Phone": request.form.get("fatherPhone"),
        "Mother's Phone": request.form.get("motherPhone"),
        "Emergency Contact 1 Name": request.form.get("emergency1Name"),
        "Emergency Contact 1 Phone": request.form.get("emergency1Phone"),
        "Emergency Contact 2 Name": request.form.get("emergency2Name"),
        "Emergency Contact 2 Phone": request.form.get("emergency2Phone"),
        "Photo/Video Consent": request.form.get("photoConsent"),
        "Pickup Authorization": request.form.get("pickupConsent"),
        "Liability Release": request.form.get("liability"),
        "Scholarship Requested": request.form.get("scholarship"),
        "Electronic Signature": request.form.get("signature")
    }

    # Validate emails
    if not validate_email(data["Email Address 1"]):
        flash("Primary email is invalid.")
        return redirect(url_for("form"))
    if not validate_email(data["Email Address 2"]):
        flash("Secondary email is invalid.")
        return redirect(url_for("form"))

    # Validate phone numbers
    for field in ["Father's Phone", "Mother's Phone", "Emergency Contact 1 Phone", "Emergency Contact 2 Phone"]:
        if not validate_phone(data[field]):
            flash(f"{field} must be 10 digits.")
            return redirect(url_for("form"))

    # Load existing registrations safely
    try:
        with open("registration.json", "r") as f:
            registrations = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        registrations = []

    registrations.append(data)

    # Save registrations safely
    try:
        with open("registration.json", "w") as f:
            json.dump(registrations, f, indent=4)
    except Exception as e:
        flash(f"Failed to save registration: {e}")
        return redirect(url_for("form"))

    flash("Registration submitted successfully!")
    return redirect(url_for("form"))

# -------------------------
# Run the app
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
