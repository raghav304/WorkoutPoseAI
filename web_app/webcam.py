import cv2

def get_camera_feed(cam_id=0):
    cap = cv2.VideoCapture(cam_id)
    if not cap.isOpened():
        st.error("Cannot open webcam.")
        return None
    
    return cap
