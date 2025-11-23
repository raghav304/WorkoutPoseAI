# 🏋️‍♂️ AI Workout Form Trainer  
**Real-Time Exercise Detection Using MediaPipe + OpenCV + Streamlit**

The **AI Workout Form Trainer** is a real-time, webcam-based fitness assistant that analyzes your exercise form using MediaPipe Pose, tracks joint angles, and counts reps accurately using a state-machine approach.

It currently supports:

- Bicep Curls  
- Shoulder Press  
- Squats  

Works with any webcam — including your **phone camera via DroidCam**.

---

## 🚀 Features

### ✔ Real-Time Pose Estimation
- Uses MediaPipe’s 33-landmark Pose model to extract body joints from the webcam feed.

### ✔ Angle-Based Rep Counting
- Computes joint angles (elbow, knee) using vector geometry.
- Applies **angle smoothing** to avoid jitter.

### ✔ Accurate State-Machine Logic
Reps are counted only when the user performs a **full movement cycle**:

`up → down → up`

with minimum frame thresholds to avoid false positives and double-counting.

### ✔ Multi-Exercise Support

Each exercise has its own joint targets and angle thresholds:

| Exercise       | Angle Tracked | Threshold Logic                          |
|----------------|--------------|------------------------------------------|
| Bicep Curl     | Elbow        | > 145° (down), < 55° (up)                |
| Shoulder Press | Elbow        | < 105° (down), > 155° (up)               |
| Squat          | Knee         | > 170° (standing/up), < 100° (bottom)    |

### ✔ Streamlit Web Interface

- Dropdown exercise selection  
- Live webcam feed rendered in the browser  
- Real-time rep counter & feedback overlay on video  
- Sidebar session stats (can be extended further)

---

## 📦 Tech Stack

- **Python 3.x**
- **MediaPipe Pose** – pose estimation
- **OpenCV** – video capture & drawing
- **NumPy** – angle calculations
- **Streamlit** – web UI

---

## 📁 Project Structure

```bash
WorkoutPoseAI/
│
├── web_app/
│   ├── streamlit_main.py      # Main Streamlit app (web UI + camera loop)
│   └── exercise_logic.py      # Rep counting + angle & form logic
│
├── utils/
│   └── angle_utils.py         # Angle calculation helper (vector math)
│
├── exercises/                 # (Optional: old standalone scripts for testing)
│   ├── bicep_curl.py
│   ├── shoulder_press.py
│   └── squat.py (if created separately)
│
├── pose_webcam.py             # Basic MediaPipe webcam pose test
├── test_cam.py                # Camera index tester
├── camera_view.py             # Simple webcam preview helper
│
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation (this file)

```
---

## 🛠 Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/raghav304/WorkoutPoseAI.git
cd WorkoutPoseAI
```
### 2️⃣ Create a virtual environment

```bash
python -m venv venv
```
### 3️⃣ Activate the venv (Windows PowerShell)

```bash
.\venv\Scripts\Activate.ps1
```
### If PowerShell blocks scripts:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```
### 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```
### ▶️ Running the App
```bash
streamlit run web_app/streamlit_main.py
```
### This will open the app in your browser.

In the app:

1. Select Bicep Curl / Shoulder Press / Squat

2. Click Start Workout

3. Stand in front of your webcam / DroidCam

4. Reps will be counted live on the video feed

## 🧠 How It Works
### 1️⃣ Pose Estimation
#### MediaPipe detects 33 body landmarks per frame.

### 2️⃣ Angle Calculation
#### Joint triplets:

- Bicep Curl → shoulder–elbow–wrist

- Shoulder Press → shoulder–elbow–wrist

- Squat → hip–knee–ankle

### 3️⃣ Angle Smoothing
```text
smooth_angle = α * prev + (1 − α) * current
```
### 4️⃣ Rep Counting (Finite State Machine)
```text
if angle < down_threshold:
    stage = "down"

if stage == "down" AND angle > up_threshold:
    reps += 1
    stage = "up"
```
#### This prevents double-counting and improves accuracy.

## 📈 Future Enhancements
### 
- Add pushups, lunges, deadlifts

- Voice feedback (“Good rep!”, “Go deeper!”)

- Workout analytics dashboard

- Deploy on Streamlit Cloud / HuggingFace

- Left–right form symmetry detection

## 🤝 Contributing
#### Contributions are welcome!
Feel free to fork the repo and open a PR.

## 📬 Contact
#### Developer: Raghav Varma

GitHub: https://github.com/raghav304

Project Repo: https://github.com/raghav304/WorkoutPoseAI





















