from src.database.config import supabase
import bcrypt
import streamlit as st
from typing import Any, cast




def hash_pass(password):
    return bcrypt.hashpw(password.encode() , bcrypt.gensalt()).decode()


def check_pass(password , hashed):
    return bcrypt.checkpw(password.encode() , hashed.encode())




def check_teacher_exist(username):
    response=supabase.table("teachers").select("username").eq("username" , username).execute()
    return len(response.data) > 0 




def create_teacher(username, password, name):
    data = {
        "username": username,
        "password": hash_pass(password),
        "name": name
    }
    print("KEY:", st.secrets["SUPABASE_PUBLISHABLE_KEY"][:20])
    print("DATA:", data)
    try:
        response = supabase.table("teachers").insert(data).execute()
        print("RESPONSE DATA:", response.data)
        print("RESPONSE:", response)
        return response.data
    except Exception as e:
        print("ERROR:", e)
        raise


def teacher_login(username, password):
    response = supabase.table("teachers").select("*").eq("username", username).execute()
    if response.data:
        teacher = cast(dict[str, Any], response.data[0])
        if check_pass(password, teacher['password']):
            return teacher
    return False




def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data




def create_student(new_name , face_embedding=None , voice_embedding=None):
    data = {"name" : new_name , "face_embedding" : face_embedding , "voice_embedding" : voice_embedding}
    response = supabase.table("students").insert(data).execute()
    return response.data






def create_subject(subject_code , name , section , teacher_id):
    data = {"subject_code" : subject_code , "name" : name , "section" : section , "teacher_id" : teacher_id}
    response = supabase.table("subjects").insert(data).execute() #type:ignore
    return response.data





def get_teacher_subject(teacher_id):
    response = supabase.table("subjects").select("* , subjects_students(count) , attendance(timestamp)").eq("teacher_id" , teacher_id).execute()
    subjects = response.data
    for sub in subjects:
        sub["total_student"] = sub.get("subjects_students" , [{}])[0].get("count" , 0) if sub.get("subjects_students") else 0 #type: ignore
        attendance = sub.get("attendance_logs" , []) #type:ignore
        unique_sections = len(set(log["timestamp"] for log in attendance)) #type:ignore
        sub["total_classes"] = unique_sections#type:ignore
        sub.pop("subjects_students" , None)#type:ignore
        sub.pop("attendance logs" , None)#type:ignore
        # print(sub)
    return subjects





def enroll_student_to_subject(student_id , subject_id):
    data = {"student_id" : student_id , "subject_id" : subject_id}
    response= supabase.table('subjects_students').insert(data).execute()
    return response.data





def unenroll_student_to_subject(student_id , subject_id):
    # data = {"student_id" : student_id , "subject_id" : subject_id}
    response= supabase.table('subjects_students').delete().eq("student_id" , student_id).eq("subject_id" , subject_id).execute()
    return response.data





def get_student_subjects(student_id):
    data = supabase.table("subjects_students").select('*, subjects(*)').eq("student_id" , student_id).execute()
    return data.data




def get_student_attendance(student_id):
    data = supabase.table("attendance").select("* , subjects(*)").eq("student_id" , student_id).execute()
    return data.data



def create_attendance(logs):
    response = supabase.table("attendance").insert(logs).execute()
    return response.data


def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendance').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
    return response.data