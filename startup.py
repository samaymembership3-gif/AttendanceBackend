import os
import requests
from storage import load_students

KNOWN_DIR = "known_people"

def rebuild_face_db():
    students = load_students()
    os.makedirs(KNOWN_DIR, exist_ok=True)

    for s in students:
        person_dir = os.path.join(KNOWN_DIR, s["roll_no"])
        os.makedirs(person_dir, exist_ok=True)

        face_path = os.path.join(person_dir, "face.jpg")

        if not os.path.exists(face_path):
            r = requests.get(s["image_url"], timeout=10)
            with open(face_path, "wb") as f:
                f.write(r.content)

    print(f"✅ Face DB rebuilt for {len(students)} students")
