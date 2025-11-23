import cv2
import mediapipe as mp
from utils.angle_utils import calculate_angle

CAM_ID = 0

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def run():
    cap = cv2.VideoCapture(CAM_ID)
    stage = None
    reps = 0

    with mp_pose.Pose(
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:

        while True:
            success, frame = cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)

            if results.pose_landmarks:
                lm = results.pose_landmarks.landmark

                shoulder = (lm[11].x*w, lm[11].y*h)
                elbow = (lm[13].x*w, lm[13].y*h)
                wrist = (lm[15].x*w, lm[15].y*h)

                elbow_angle = calculate_angle(shoulder, elbow, wrist)

                cv2.putText(frame, str(int(elbow_angle)),
                            (int(elbow[0]), int(elbow[1])-20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

                # Rep Logic
                if elbow_angle > 150:
                    stage = "down"
                if elbow_angle < 40 and stage == "down":
                    stage = "up"
                    reps += 1

                cv2.putText(frame, f"Reps: {reps}", 
                            (30, 80),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.5, (255,255,255), 3)

                # Form check example
                if wrist[0] < shoulder[0] - 30:
                    form = "Keep wrist aligned!"
                else:
                    form = "Good form"

                cv2.putText(frame, form, 
                            (30, 130),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0, (0,255,255), 2)

                mp_drawing.draw_landmarks(frame,
                                          results.pose_landmarks,
                                          mp_pose.POSE_CONNECTIONS)

            cv2.imshow("Bicep Curl - Press Q", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
