from deepface import DeepFace
import os
import cv2
import uuid

KNOWN_DIR = "known_people"
TEMP_DIR = "temp"

os.makedirs(TEMP_DIR, exist_ok=True)

def identify_students(group_image_path: str):
    faces = DeepFace.extract_faces(
        img_path=group_image_path,
        detector_backend="retinaface",
        enforce_detection=False
    )

    identified = set()

    for face in faces:
        face_img = face["face"]
        temp_path = os.path.join(TEMP_DIR, f"{uuid.uuid4()}.jpg")
        cv2.imwrite(temp_path, face_img)

        try:
            result = DeepFace.find(
                img_path=temp_path,
                db_path=KNOWN_DIR,
                model_name="ArcFace",
                enforce_detection=False
            )

            if len(result) > 0 and len(result[0]) > 0:
                identity = result[0].iloc[0]["identity"]
                roll_no = identity.split(os.sep)[-2]
                identified.add(roll_no)
        except:
            pass

        os.remove(temp_path)

    return list(identified)
