import cv2

print("Scanning for cameras...")
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"✅ Camera found at index: {i}")
        cap.release()
