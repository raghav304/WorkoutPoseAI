import cv2
import mediapipe as mp
from angle_utils import calculate_angle

CAM_ID = 0  # your phone webcam

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def main():
    cap = cv2.VideoCapture(CAM_ID)
    if not cap.isOpened():
        print("❌ Cannot open camera.")
        return
    
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
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)

            if results.pose_landmarks:

                landmarks = results.pose_landmarks.landmark
                h, w, _ = frame.shape

                hip = (landmarks[23].x*w, landmarks[23].y*h)
                knee = (landmarks[25].x*w, landmarks[25].y*h)
                ankle = (landmarks[27].x*w, landmarks[27].y*h)

                knee_angle = calculate_angle(hip, knee, ankle)

                cv2.putText(frame, str(int(knee_angle)),
                            (int(knee[0]), int(knee[1])-20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

                # Squat Logic
                if knee_angle > 160:
                    feedback = "Standing"
                elif knee_angle > 100:
                    feedback = "Going Down"
                else:
                    feedback = "Good Squat Depth"

                cv2.putText(frame, feedback, (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,0,0), 3)

                mp_drawing.draw_landmarks(frame,
                                          results.pose_landmarks,
                                          mp_pose.POSE_CONNECTIONS)

            cv2.imshow("Squat Analysis - Press Q to exit", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
