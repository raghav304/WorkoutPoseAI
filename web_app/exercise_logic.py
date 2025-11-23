import cv2
import mediapipe as mp
from utils.angle_utils import calculate_angle

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils


def smooth_angle(prev, current, alpha=0.6):
    """Smooth sudden jumps in angle values for stability."""
    return alpha * prev + (1 - alpha) * current


def process_frame(exercise, frame):
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = exercise["pose"].process(rgb)

    reps = exercise.get("reps", 0)
    phase = exercise.get("phase", "up")          # "up" or "down"
    went_down = exercise.get("went_down", False) # did we hit bottom?
    frames_up = exercise.get("frames_up", 0)
    frames_down = exercise.get("frames_down", 0)

    feedback = ""
    display_angle = 0

    if results.pose_landmarks:
        lm = results.pose_landmarks.landmark

        # ----------------------- SELECT JOINTS BY EXERCISE -----------------------
        if exercise["name"] in ["Bicep Curl", "Shoulder Press"]:
            # LEFT ARM joints
            shoulder = (lm[11].x * w, lm[11].y * h)
            elbow = (lm[13].x * w, lm[13].y * h)
            wrist = (lm[15].x * w, lm[15].y * h)

            raw_angle = calculate_angle(shoulder, elbow, wrist)
            angle_label = "Elbow Angle"

        elif exercise["name"] == "Squat":
            # LEFT LEG joints
            hip = (lm[23].x * w, lm[23].y * h)
            knee = (lm[25].x * w, lm[25].y * h)
            ankle = (lm[27].x * w, lm[27].y * h)

            raw_angle = calculate_angle(hip, knee, ankle)
            angle_label = "Knee Angle"

        else:
            raw_angle = 0
            angle_label = "Angle"

        # -------------------------- ANGLE SMOOTHING --------------------------
        raw_angle = max(0, min(180, raw_angle))  # clamp for safety
        smoothed = smooth_angle(exercise.get("prev_angle", raw_angle), raw_angle)
        exercise["prev_angle"] = smoothed
        display_angle = smoothed

        # -------------------------- THRESHOLDS --------------------------
        # You can tweak these for your style later
        if exercise["name"] == "Bicep Curl":
            up_thresh = 166   # arm almost straight
            down_thresh = 53  # arm fully flexed
            min_down_frames = 3
            min_up_frames = 3

        elif exercise["name"] == "Shoulder Press":
            down_thresh = 105  # bar at shoulder
            up_thresh = 155    # arms locked out
            min_down_frames = 3
            min_up_frames = 3

        elif exercise["name"] == "Squat":
            up_thresh = 170    # standing tall
            down_thresh = 100  # deep squat
            min_down_frames = 3
            min_up_frames = 3

        else:
            up_thresh = 999
            down_thresh = -999
            min_down_frames = 3
            min_up_frames = 3

        # -------------------------- PHASE LOGIC --------------------------
        # We want: up (start) -> down (bottom) -> up (finish) = 1 rep

        # Are we in "down" zone?
        in_down = smoothed < down_thresh
        # Are we in "up" zone?
        in_up = smoothed > up_thresh

        if in_down:
            frames_down += 1
            frames_up = 0
        elif in_up:
            frames_up += 1
            frames_down = 0
        else:
            # mid-range, not fully up or down
            frames_up = 0
            frames_down = 0

        # Hit bottom long enough
        if in_down and frames_down >= min_down_frames:
            phase = "down"
            went_down = True

        # Came back up long enough after going down -> count rep
        if in_up and went_down and frames_up >= min_up_frames:
            phase = "up"
            reps += 1
            went_down = False

            if exercise["name"] == "Bicep Curl":
                feedback = "Nice curl!"
            elif exercise["name"] == "Shoulder Press":
                feedback = "Good lockout!"
            elif exercise["name"] == "Squat":
                feedback = "Good depth!"

        # Extra squat-specific feedback for shallow reps
        if exercise["name"] == "Squat" and phase == "up":
            if down_thresh < smoothed < (up_thresh - 10):
                feedback = "Go deeper!"

        # -------------------------- DRAW OVERLAYS ---------------------------
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Reps
        cv2.putText(
            frame, f"Reps: {reps}", (30, 80),
            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2
        )

        # Angle
        cv2.putText(
            frame, f"{angle_label}: {int(display_angle)}",
            (30, 130),
            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2
        )

        # Feedback
        if feedback:
            cv2.putText(
                frame, feedback, (30, 180),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2
            )

    # -------------------------- SAVE STATE BACK --------------------------
    exercise["reps"] = reps
    exercise["phase"] = phase
    exercise["went_down"] = went_down
    exercise["frames_up"] = frames_up
    exercise["frames_down"] = frames_down

    return frame, reps, phase
