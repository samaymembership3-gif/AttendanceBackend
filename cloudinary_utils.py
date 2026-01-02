import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv
load_dotenv()  # loads variables from .env

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def upload_face(image_path: str, roll_no: str):
    result = cloudinary.uploader.upload(
        image_path,
        folder="attendance_faces",
        public_id=roll_no,
        overwrite=True
    )
    return result["secure_url"]
