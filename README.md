# SnapAI Class 🎓🤖

> **AI-powered attendance management system using Face Recognition and Voice Recognition.**

SnapAI Class is an intelligent attendance management platform designed to make classroom attendance **automated, secure, and convenient**.

Instead of relying on traditional roll calls or manual attendance, SnapAI Class uses **Face Recognition and Voice Recognition** to identify students and record their attendance.

## ✨ Features

* 📸 **Face Recognition Attendance**

  * Identifies students using facial embeddings.
  * Automatically marks attendance.

* 🎙️ **Voice Recognition**

  * Uses voice embeddings for student verification.
  * Provides an additional layer of identity verification.

* 👨‍🎓 **Student Management**

  * Register students.
  * Store student information securely.
  * Manage enrolled subjects.

* 📚 **Subject & Enrollment Management**

  * Create and manage subjects.
  * Support different sections.
  * Students can enroll in subjects.

* 🔐 **Authentication & Authorization**

  * Secure user authentication.
  * Role-based access for students and teachers.

* 📊 **Attendance Dashboard**

  * View attendance records.
  * Track student attendance across subjects.

* 🗄️ **Cloud Database**

  * Supabase-powered backend.
  * PostgreSQL database with Row Level Security.

## 🧠 How It Works

```text
                 ┌──────────────────┐
                 │      Student     │
                 └────────┬─────────┘
                          │
                Face / Voice Input
                          │
                          ▼
                 ┌──────────────────┐
                 │   AI Pipeline    │
                 │                  │
                 │ Face Recognition │
                 │ Voice Recognition│
                 └────────┬─────────┘
                          │
                    Verification
                          │
                          ▼
                 ┌──────────────────┐
                 │    Attendance    │
                 │     System      │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │     Supabase     │
                 │    PostgreSQL    │
                 └──────────────────┘
```

## 🛠️ Tech Stack

### Frontend / UI

* Python
* Streamlit

### AI / Machine Learning

* Python
* OpenCV
* dlib
* face_recognition
* scikit-learn
* Librosa
* Resemblyzer
* NumPy
* Pandas

### Backend / Database

* Supabase
* PostgreSQL
* Supabase Authentication
* Row Level Security (RLS)

### Deployment

* Streamlit Cloud
* Vercel

## 📁 Project Structure

=AI_Attendance/
│
├── app.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── components/
│   ├── database/
│   ├── pipelines/
│   │   ├── face_pipeline.py
│   │   └── voice_pipeline.py
│   │── screens
│   └── ui/
│


## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/SnapAI-Class.git
cd AI_Attedance
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file and add your Supabase credentials:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```


### 5. Run the application

```bash
streamlit run app.py
```

The application will be available locally at:

```text
http://localhost:8501
```

## 🔐 Security

SnapAI Class uses **Supabase Row Level Security (RLS)** to control access to database records.

Sensitive credentials are stored using environment variables rather than being hard-coded into the application.

## 🎯 Why SnapAI Class?

Traditional attendance systems can be:

* Time-consuming
* Manual
* Prone to proxy attendance
* Difficult to manage for large classrooms

SnapAI Class aims to reduce manual work while providing a more reliable identity-based attendance process.

## 🚀 Future Improvements

*  Advanced teacher analytics dashboard

## 🌐 Live Demo

**Landing Page:**
https://landing-page-snap-class.vercel.app/

**AI Attendance Application:**
https://snapaiclass.streamlit.app/

## 👨‍💻 Author

**Yash Gupta**

B.Tech — Computer Science Engineering (AI)
Institute of Engineering and Technology, Lucknow

---

⭐ If you find AI_ATTENDANCE Class interesting, consider giving the repository a star!
