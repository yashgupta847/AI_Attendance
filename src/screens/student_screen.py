import streamlit as st
from src.ui.stylebase_layout import style_base_layout , style_base_home , style_base_dashboard
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.pipelines.face_pipeline import predict_attendance , get_face_embeddings
from src.pipelines.voice_pipeline import get_voice_embedding
from src.pipelines.face_pipeline import train_classifier
from src.database.db import create_student , get_student_subjects , get_student_attendance , get_all_students , unenroll_student_to_subject
from src.components.dialog_enroll_student_subject import enroll_dialog
from src.components.dialog_subject_card import subject_card

def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data["student_id"]
    c1, c2 = st.columns(2, vertical_alignment='center', gap='large')
    with c1:
            header_dashboard()
    with c2:
            st.subheader(f"""Welcome, {student_data["name"]}""")
            if st.button("Logout" ,type="secondary" , key="loginbackbtn" , shortcut="control+backspace"):
                st.session_state["is_logged_in"] = False
                del st.session_state.student_data
                st.rerun()
            
    st.space()   
    c1 , c2 = st.columns(2)
    with c1:
        st.header("Your Enrolled Subjects")
    with c2:
        if st.button("Enroll in Subject" , type="primary" , width='stretch'):
            enroll_dialog()

    st.divider()
    with st.spinner("Loading Your Subjects...."):
        subjects = get_student_subjects(student_id)
        attendance_logs = get_student_attendance(student_id)
        stats_map = {}
        for log in attendance_logs:
            sid = log['subject_id'] #type:ignore
            if sid not in stats_map:
                stats_map[sid] = {"total" : 0 , "attended" : 0}
            stats_map[sid]["total"] += 1 #type:ignore
            if log.get("is_present"): #type:ignore
                stats_map[sid]["attended"] += 1 #type:ignore
        cols = st.columns(2)
        for i , sub_node in enumerate(subjects):
            sub = sub_node["subjects"] #type:ignore
            sid = sub["subject_id"] #type:ignore
            stats = stats_map.get(sid , {"total" : 0 , "attended" : 0}) #type:ignore
            def unenroll_button():
                if st.button("Unenroll from this course", type='tertiary', width='stretch', icon=':material/delete_forever:' , key=f"unenroll_{student_id}_{sid}"):
                    unenroll_student_to_subject(student_id, sid)
                    st.toast(f"Unenrolled from {sub['name']} successfully!") #type:ignore
                    st.rerun()
                    
            with cols[i%2]:
                subject_card( 
                        name = sub['name'], #type:ignore
                        code =sub['subject_code'], #type:ignore
                        section = sub['section'], #type:ignore
                        stats = [
                            ('📅', 'Total', stats['total']),
                            ('✅', 'Attended', stats['attended']),
                        ],
                        footer_callback=unenroll_button
                )
        footer_dashboard()






     
def student_screen():
    style_base_layout()
    style_base_dashboard()

    if "student_data" in st.session_state:
        student_dashboard()
        return
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
            header_dashboard()
    with c2:
            if st.button("Go back to home" ,type="secondary" , key="loginbackbtn" , shortcut="control+backspace"):
                st.session_state["login_state"] = None
                st.rerun()
    st.header("Login using faceID" ,text_alignment="center")
    st.space()
    st.space()
    show_registration=False
    photo_source = st.camera_input("Position Your Face in the center")
    if photo_source:
        img = np.array(Image.open(photo_source))
        with st.spinner("AI is scanning..."):
            detected , all_ids , num_faces = predict_attendance(img)
            if num_faces == 0:
                st.warning("Face not found")
            elif num_faces > 1:
                st.warning("Multiple faces found")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s["student_id"] == student_id) , None) #type: ignore
                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back {student['name']}") #type: ignore
                        import time
                        time.sleep(1)
                        st.rerun()
                else:
                    st.info('Face not recognized! You might be a new student!')
                    show_registration = True
    if show_registration:
        with st.container(border=True):
            st.header('Register new Profile')
            new_name = st.text_input("Enter your name", placeholder='E.g. Hamza Rizvi')
            st.subheader('Optional : Voice Enrollment')
            st.info("Enroll your for voice only attendance")
            audio_data = None
            try:
                audio_data = st.audio_input("Record a short phrase like I am Present , My name is Akash.")
            except Exception:
                st.error("Audioi Daa failed")

            if st.button("Create Account" , type="primary"):
                if new_name:
                    with st.spinner("Creating Profile"):
                        img = np.array(Image.open(photo_source)) #type: ignore
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())
                            response_data = create_student(new_name , face_embedding=face_emb , voice_embedding=voice_emb)
                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f'Profile Created! Hi {new_name}!')
                                import time
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.error('Couldnt capture your facial features for registration')
                else :
                    st.warning("Please Enter Your name")
    footer_dashboard()