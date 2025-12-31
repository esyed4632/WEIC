from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

levels = {
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [],
    9: []
}

DATA_FILE = "registrations.json"

@app.route("/")
def index():
    return render_template("register.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    child = data["Children"][0]

    age = int(child["Age"])

    if age < 5:
        return jsonify({"error": "Too Young — can't apply"}), 400
    if age > 13:
        return jsonify({"error": "Too Old — too late"}), 400

    level = age - 4
    levels[level].append(child)

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            all_data = json.load(f)
    else:
        all_data = {str(i): [] for i in range(1, 10)}

    all_data[str(level)].append(child)

    with open(DATA_FILE, "w") as f:
        json.dump(all_data, f, indent=4)

    return jsonify({
        "message": "Registration successful",
        "assigned_level": level
    })

if __name__ == "__main__":
    app.run(debug=True)
