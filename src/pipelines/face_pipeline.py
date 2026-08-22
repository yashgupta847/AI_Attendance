import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st
from src.database.db import get_all_students
from typing import Any , cast
#DLIb provide face detector , shape predictor(landwmarks) , ResNet(facerec) -> embedding(128 Dimensions)

@st.cache_resource
def load_dlib_models():

    # 1. Face detector
    detector = dlib.get_frontal_face_detector() # type: ignore

    # 2. 68 facial landmarks predictor
    sp = dlib.shape_predictor( #type:ignore
        face_recognition_models.pose_predictor_model_location()
    )

    # 3. Face recognition model → 128-D embedding
    facerec = dlib.face_recognition_model_v1( #type:ignore
        face_recognition_models.face_recognition_model_location()
    )
    return detector, sp, facerec


def get_face_embeddings(img_np):
    detector , sp , facerec = load_dlib_models()
    faces = detector(img_np , 1)
    encodings = []
    for face in faces :
        shape = sp(img_np , face)
        face_descriptor = facerec.compute_face_descriptor(img_np , shape , 1) #128 embeddings
        encodings.append(np.array(face_descriptor))
    return encodings

@st.cache_resource
def get_trained_model():
    X = []
    Y = []
    student_db = get_all_students()
    
    if not student_db:
        return None
    for student_data in student_db:
        student = cast(dict[str, Any], student_data)
        embedding = student.get("face_embedding")
        if embedding:
            X.append(np.array(embedding))
            Y.append(student.get("student_id"))
    if len(X) == 0:
        return 0

    clf = SVC(kernel="linear" , probability=True , class_weight="balanced")
    try:
        clf.fit(X , Y)  #type: ignore
    except ValueError:
        pass
    return {"clf" : clf , "X" : X , "Y" : Y}


def train_classifier():
    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)
    detected_students = {}
    model_data = get_trained_model()
    if not model_data:
        return {} , [] , len(encodings)
    clf = model_data["clf"] #type:ignore
    X = model_data["X"] #type:ignore
    Y = model_data["Y"] #type:ignore
    all_students = sorted(list(set(Y)))
    for encoding in encodings:
        if len(all_students) >= 2:
            predicted_id = int(clf.predict([encoding])[0])
        else :
            predicted_id = int(all_students[0])
        student_embedding = X[Y.index(predicted_id)]
        best_match_score = np.linalg.norm(student_embedding - encoding)
        resemblance_threhold = 0.6
        if best_match_score <= resemblance_threhold:
            detected_students[predicted_id] = True
    return detected_students , all_students , len(encodings)