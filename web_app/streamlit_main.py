import sys
import os

# Fix Python path for importing from parent folder
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

import streamlit as st
import cv2
import mediapipe as mp
from web_app.exercise_logic import process_frame


# --------------------------- STREAMLIT SETUP ---------------------------
st.set_page_config(page_title="AI Workout Trainer", layout="wide")

st.title("💪 AI Workout Form Trainer")
st.write("Select an exercise and click Start to begin your workout.")

# Sidebar
st.sidebar.title("Session Stats")

exercise_name = st.sidebar.selectbox(
    "Choose Exercise:",
    ["Bicep Curl", "Shoulder Press", "Squat"],
    key="exercise_select"   # 👈 unique key
)

st.sidebar.write(f"Selected: **{exercise_name}**")




# --------------------------- SESSION STATE ---------------------------
if "running" not in st.session_state:
    st.session_state.running = False

if "reps" not in st.session_state:
    st.session_state.reps = 0


# --------------------------- UI ELEMENTS ---------------------------
exercise_name = st.selectbox(
    "Choose Exercise:",
    ["Bicep Curl", "Shoulder Press", "Squat"]
)


# Reset reps and start workout
if st.button("Start Workout", key="start_button"):
    st.session_state.running = True
    st.session_state.reps = 0

# Stop
st.button("Stop Workout", key="stop_button", 
          on_click=lambda: st.session_state.update(running=False))

frame_placeholder = st.empty()


# ------------ Initialize pose model for selected exercise ------------
exercise = {
    "name": exercise_name,
    "pose": mp.solutions.pose.Pose(
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ),
    "reps": 0,
    "stage": None,
    "cooldown": 0
}


# --------------------------- MAIN LOOP ---------------------------
if st.session_state.running:
    cap = cv2.VideoCapture(0)

    while st.session_state.running and cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        frame, reps, stage = process_frame(exercise, frame)

        exercise["reps"] = reps
        exercise["stage"] = stage

        st.sidebar.metric("Reps (this set)", reps)
        st.sidebar.write(f"Stage: **{stage if stage else '-'}**")


        frame_placeholder.image(frame, channels="BGR", use_column_width=True)

    cap.release()
