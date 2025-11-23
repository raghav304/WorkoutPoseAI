import cv2
import time
import mediapipe as mp

# Your phone webcam (DroidCam) is camera index 0
CAM_ID = 0

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def main():
    cap = cv2.VideoCapture(CAM_ID)
    if not cap.isOpened():
        print("❌ Error: Cannot open webcam.")
        return

    with mp_pose.Pose(
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:

        prev_time = 0

        while True:
            success, frame = cap.read()
            if not success:
                print("⚠️ Failed to read frame")
                break

            # Flip for a selfie view
            frame = cv2.flip(frame, 1)

            # Convert to RGB for MediaPipe
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)

            # Draw pose landmarks
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS
                )

            # FPS calculation
            curr_time = time.time()
            fps = int(1 / (curr_time - prev_time)) if prev_time else 0
            prev_time = curr_time

            cv2.putText(frame, f"FPS: {fps}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            # Show output
            cv2.imshow("Workout Pose Detection", frame)

            # Force the window to take focus
            cv2.setWindowProperty("Workout Pose Detection", cv2.WND_PROP_TOPMOST, 1)
            cv2.setWindowProperty("Workout Pose Detection", cv2.WND_PROP_TOPMOST, 0)

            key = cv2.waitKey(1)
            if key == ord('q') or key == 27:  # 27 = ESC
              break



cap.release()
for i in range(5):
    cv2.destroyAllWindows()
    cv2.waitKey(1)





if __name__ == "__main__":
    main()
