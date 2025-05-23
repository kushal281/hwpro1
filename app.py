from flask import Flask, request, jsonify, render_template, session, redirect, url_for, make_response
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Set a strong secret key

# Load password file
def check_password(userid, password):
    try:
        with open("password.txt") as f:
            for line in f:
                uid, pwd = line.strip().split(',')
                if int(uid) == userid and pwd == password:
                    return True
    except:
        return False
    return False

# Load student record
def load_student(userid):
    try:
        with open("index.txt") as f:
            for line in f:
                parts = line.strip().split(',')
                sid, name = int(parts[0]), parts[1]
                if sid == userid:
                    grades = []
                    for course in parts[2:]:
                        cname, score = course.split(':')
                        grades.append({'course': cname, 'grade': int(score)})
                    return {'id': sid, 'name': name, 'grades': grades}
    except:
        return None
    return None

# Update student record
def update_student(student):
    lines = []
    with open("index.txt") as f:
        for line in f:
            parts = line.strip().split(',')
            if int(parts[0]) == student['id']:
                new_line = f"{student['id']},{student['name']}"
                for g in student['grades']:
                    new_line += f",{g['course']}:{g['grade']}"
                lines.append(new_line)
            else:
                lines.append(line.strip())
    with open("index.txt", 'w') as f:
        for line in lines:
            f.write(line + "\n")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/options")
def options():
    if "userid" not in session:
        return redirect(url_for("home"))
    return render_template("options.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if check_password(data["userid"], data["password"]):
        session["userid"] = data["userid"]  # Set session on login
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Invalid credentials"})

@app.route("/logout")
def logout():
    session.pop("userid", None)  # Clear session on logout
    return redirect(url_for("home"))

@app.route("/record/<int:userid>", methods=["GET"])
def record(userid):
    # Check session for authentication
    if "userid" not in session or int(session["userid"]) != userid:
        return jsonify({"error": "Unauthorized"}), 401
    student = load_student(userid)
    if student:
        return jsonify(student)
    return jsonify({"error": "Student not found"}), 404

@app.route("/record/<int:userid>/add", methods=["POST"])
def add_course(userid):
    # Check session for authentication
    if "userid" not in session or int(session["userid"]) != userid:
        return jsonify({"error": "Unauthorized"}), 401
    student = load_student(userid)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    if len(student['grades']) >= 4:
        return jsonify({"error": "Course limit reached"}), 400

    new_course = request.json
    student['grades'].append({'course': new_course['course'], 'grade': new_course['grade']})
    update_student(student)
    return jsonify({"message": "Course added successfully"})

@app.route("/record/<int:userid>/remove/<string:course>", methods=["DELETE"])
def remove_course(userid, course):
    # Check session for authentication
    if "userid" not in session or int(session["userid"]) != userid:
        return jsonify({"error": "Unauthorized"}), 401
    student = load_student(userid)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    initial_count = len(student['grades'])
    student['grades'] = [g for g in student['grades'] if g['course'].lower() != course.lower()]
    if len(student['grades']) == initial_count:
        return jsonify({"error": "Course not found"}), 404
    update_student(student)
    return jsonify({"message": f"Course '{course}' removed successfully"})

# Prevent caching of protected pages
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == "__main__":
    app.run(debug=True)
# if __name__ == "__main__":
#    app.run(debug=True, host="0.0.0.0")