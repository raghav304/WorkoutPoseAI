import cv2

CAM_ID = 0  # try 0 first

cap = cv2.VideoCapture(CAM_ID)

if not cap.isOpened():
    print(f"❌ Camera {CAM_ID} failed to open")
    exit()

print(f"✅ Camera {CAM_ID} opened successfully. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to read frame.")
        break

    cv2.imshow(f"Camera {CAM_ID}", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
