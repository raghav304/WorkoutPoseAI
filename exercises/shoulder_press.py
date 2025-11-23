import cv2
import mediapipe as mp
from angle_utils import calculate_angle

CAM_ID = 0  # Your phone camera index

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def main():
    cap = cv2.VideoCapture(CAM_ID)
    if not cap.isOpened():
        print("❌ Cannot open camera.")
        return

    # Rep counting variables
    stage = None   # "up" or "down"
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
                landmarks = results.pose_landmarks.landmark

                # LEFT ARM (use right side if left is occluded)
                shoulder = (landmarks[11].x*w, landmarks[11].y*h)
                elbow = (landmarks[13].x*w, landmarks[13].y*h)
                wrist = (landmarks[15].x*w, landmarks[15].y*h)

                # Calculate elbow angle
                elbow_angle = calculate_angle(shoulder, elbow, wrist)

                # Show angle near elbow
                cv2.putText(frame, str(int(elbow_angle)),
                            (int(elbow[0]), int(elbow[1]) - 20),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (0,255,0), 2)

                # ----- REP COUNTING LOGIC -----
                if elbow_angle < 100:  
                    stage = "down"

                if elbow_angle > 160 and stage == "down":
                    stage = "up"
                    reps += 1

                # Display reps
                cv2.putText(frame, f"Reps: {reps}",
                            (30, 80),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.5, (255,255,255), 3)

                # ----- FORM CHECK -----
                # Check elbow flare – shoulder should be aligned
                shoulder_y = shoulder[1]
                elbow_y = elbow[1]

                if elbow_y < shoulder_y - 20:
                    form_feedback = "Elbows too high!"
                else:
                    form_feedback = "Good form"

                cv2.putText(frame, form_feedback,
                            (30, 130),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0, (0,255,255), 2)

                # Draw skeleton
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS
                )

            cv2.imshow("Shoulder Press - Press Q to exit", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
