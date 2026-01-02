import json
import os

DB_FILE = "students.json"

def load_students():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_students(students):
    with open(DB_FILE, "w") as f:
        json.dump(students, f, indent=2)

def add_student(roll_no, name, image_url):
    students = load_students()
    students = [s for s in students if s["roll_no"] != roll_no]

    students.append({
        "roll_no": roll_no,
        "name": name,
        "image_url": image_url
    })

    save_students(students)

def delete_student(roll_no):
    students = load_students()
    students = [s for s in students if s["roll_no"] != roll_no]
    save_students(students)
