from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import os
import uuid
import shutil

from cloudinary_utils import upload_face
from storage import add_student, delete_student, load_students
from face_utils import identify_students
from startup import rebuild_face_db

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="Attendance System Backend")

# 🔥 Startup Event
@app.on_event("startup")
def startup_event():
    rebuild_face_db()

# --------------------------------------------------
# 1️⃣ REGISTER STUDENT
# --------------------------------------------------
@app.post("/register")
async def register_student(
    name: str = Form(...),
    roll_no: str = Form(...),
    file: UploadFile = File(...)
):
    temp_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.jpg")

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    image_url = upload_face(temp_path, roll_no)
    add_student(roll_no, name, image_url)

    os.remove(temp_path)
    rebuild_face_db()

    return {
        "status": "success",
        "roll_no": roll_no,
        "name": name
    }

# --------------------------------------------------
# 2️⃣ TAKE ATTENDANCE
# --------------------------------------------------
@app.post("/attendance")
async def take_attendance(file: UploadFile = File(...)):
    temp_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}.jpg")

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    rolls = identify_students(temp_path)
    os.remove(temp_path)

    students = load_students()
    present = [
        s for s in students if s["roll_no"] in rolls
    ]

    return {
        "count": len(present),
        "students": present
    }

# --------------------------------------------------
# 3️⃣ DELETE STUDENT
# --------------------------------------------------
@app.delete("/delete/{roll_no}")
def remove_student(roll_no: str):
    delete_student(roll_no)
    rebuild_face_db()
    return {"status": "deleted", "roll_no": roll_no}
