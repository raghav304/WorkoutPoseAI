🏋️‍♂️ AI Workout Form Trainer
Real-Time Exercise Detection Using MediaPipe + OpenCV + Streamlit

The AI Workout Form Trainer is a real-time, webcam-based fitness assistant that analyzes your exercise form using MediaPipe Pose, tracks your joint angles, and counts reps accurately using a state-machine approach.
It currently supports:

Bicep Curls

Shoulder Press

Squats

Built with Python, OpenCV, MediaPipe, and Streamlit, this project works with any webcam — including your phone camera via apps like DroidCam.

🚀 Features
✔ Real-Time Pose Estimation

Uses MediaPipe’s 33 landmark Pose model to extract joint positions from webcam feed.

✔ Angle-Based Rep Counting

Computes joint angles (elbow, knee) using vector geometry and applies smoothing to avoid jitter.

✔ Accurate State-Machine Rep Logic

Reps are counted only when the user performs a full cycle:
up → down → up
with minimum frame requirements to avoid miscounts.

✔ Multi-Exercise Support

Each exercise has its own joint targets and thresholds:

Exercise	Angle Tracked	Threshold Logic
Bicep Curl	Elbow	>145° (down), <55° (up)
Shoulder Press	Elbow	<105° (down), >155° (up)
Squat	Knee	>170° (up), <100° (down)
✔ Streamlit Web Interface

User-friendly web app with:

Dropdown exercise selection

Live webcam feed

Sidebar session stats

Real-time reps & feedback overlay

📦 Tech Stack

Python 3.x

MediaPipe Pose (pose estimation)

OpenCV (video capture & drawing)

Streamlit (web interface)

NumPy (angle calculations)

📁 Project Structure
WorkoutPoseAI/
│
├── web_app/
│   ├── streamlit_main.py        # Main Streamlit app
│   └── exercise_logic.py        # Rep counting + angle logic
│
├── utils/
│   └── angle_utils.py           # Angle calculation helper
│
├── exercises/                   # (Optional: old standalone scripts)
│
├── pose_webcam.py               # Basic MediaPipe test
├── test_cam.py                  # Camera tester
├── camera_view.py               # Webcam helper
│
├── requirements.txt             # Python dependencies
└── README.md                    # (This file)

🛠️ Installation
1. Clone the repository
git clone https://github.com/raghav304/WorkoutPoseAI.git
cd WorkoutPoseAI

2. Create a virtual environment
python -m venv venv

3. Activate the venv (Windows)
.\venv\Scripts\Activate.ps1


If PowerShell blocks scripts:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1

4. Install dependencies
pip install -r requirements.txt

▶️ Running the App
streamlit run web_app/streamlit_main.py


This will open a browser window.

In the app:

Select Bicep Curl / Shoulder Press / Squat

Click Start Workout

Stand in front of your webcam or phone (DroidCam)

Start exercising — reps will appear in real time!

🧠 How It Works
1. Pose Estimation (MediaPipe)

The webcam frame is passed to MediaPipe Pose, which outputs 33 landmarks.

2. Angle Calculation

For each exercise, specific joints are tracked:

Bicep Curl → shoulder–elbow–wrist

Shoulder Press → shoulder–elbow–wrist

Squat → hip–knee–ankle

Using vector math, we compute the angle at the joint.

3. Angle Smoothing

Raw angles fluctuate → we apply exponential smoothing:

smooth = α * prev + (1 − α) * current

4. Rep Counting (Finite State Machine)

Example for Squat:

if angle < down_thresh → phase = "down"
if phase == "down" AND angle > up_thresh → rep++


Minimum frame requirements stop false triggers.

📈 Future Enhancements

Add pushups, lunges, deadlifts

Add voice feedback (“Good rep!”, “Go deeper!”)

Add session analytics dashboard

Deploy the app on Streamlit Cloud / HuggingFace Spaces

Add left-right symmetry detection

🤝 Contributing

Feel free to fork the repo and submit PRs for new exercises or improvements!

📬 Contact

Built by Raghav Varma
GitHub: https://github.com/raghav304