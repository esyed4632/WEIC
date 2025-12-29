from flask import Flask, render_template, request, redirect, url_for, flash
import json
import re

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages

# -------------------------
# Validation functions
# -------------------------
def validate_email(email):
    if not email:
        return True  # Optional secondary email
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_phone(phone):
    return re.match(r"^\d{10}$", phone)  # 10-digit phone number

# -------------------------
# Routes
# -------------------------
@app.route("/", methods=["GET"])
def form():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    data = {
        "Child": {
            "Name": request.form.get("childName"),
            "Gender": request.form.get("gender"),
            "Date of Birth": request.form.get("dob"),
            "Age": request.form.get("age"),
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

    # -------------------------
    # Validate required fields
    # -------------------------
    if not validate_email(data["Email Address 1"]):
        flash("Primary email is invalid.")
        return redirect(url_for("form"))

    for phone_field in ["Father's Phone", "Mother's Phone", "Emergency Contact 1 Phone", "Emergency Contact 2 Phone"]:
        if not validate_phone(data[phone_field]):
            flash(f"{phone_field} must be 10 digits.")
            return redirect(url_for("form"))

    # -------------------------
    # Save to registration.json
    # -------------------------
    try:
        with open("registration.json", "r") as f:
            registrations = json.load(f)
    except FileNotFoundError:
        registrations = []

    registrations.append(data)

    with open("registration.json", "w") as f:
        json.dump(registrations, f, indent=4)

    flash("Registration submitted successfully!")
    return redirect(url_for("form"))

# -------------------------
# Run the app
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
