# AI Workout Form Trainer 🏋️‍♂️

A real-time AI fitness assistant that analyzes your form and counts reps for:
- Bicep Curls
- Shoulder Press
- Squats

Built with:
- MediaPipe Pose (pose estimation)
- OpenCV (video processing)
- Streamlit (web UI)

## Features

- Real-time joint angle tracking from webcam / phone (DroidCam)
- Angle-based rep counting with smoothing + cooldown to avoid miscounts
- Separate logic for each exercise (elbow angles for curls/press, knee angle for squats)
- Simple Streamlit interface with exercise selection

## How to Run

```bash
git clone <your-repo-url>
cd WorkoutPoseAI
python -m venv venv
# activate venv...
pip install -r requirements.txt
streamlit run web_app/streamlit_main.py
