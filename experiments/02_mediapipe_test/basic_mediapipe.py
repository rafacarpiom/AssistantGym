"""
Basic MediaPipe Pose experiment.

Goal:
- Open a video with OpenCV
- Run MediaPipe Pose on each frame
- Draw pose landmarks and show the result.
"""

from pathlib import Path

import cv2
import mediapipe as mp

# 1. Paths and video loading

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
VIDEO_PATH = PROJECT_ROOT / "data" / "raw" / "Sentadilla.mp4"

if not VIDEO_PATH.exists():
    print(f"Error: Video file not found at {VIDEO_PATH}")
    exit(1)

cap = cv2.VideoCapture(str(VIDEO_PATH))

if not cap.isOpened():
    print(f"Error: Could not open video file at {VIDEO_PATH}")
    exit(1)

# 2. MediaPipe Pose setup

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Create a pose object

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Configure window to be resizable
cv2.namedWindow("MediaPipe Pose - Basic demo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("MediaPipe Pose - Basic demo", 720, 1280)

# 3. Main processing loop

while True: 
    ret, frame = cap.read()
    if not ret:
        print("End of the video")
        break

    # Resize frame to fit screen while maintaining aspect ratio
    h, w = frame.shape[:2]
    max_display_width = 720
    if w > max_display_width:
        scale = max_display_width / w
        display_width = max_display_width
        display_height = int(h * scale)
        frame = cv2.resize(frame, (display_width, display_height))

    # OpenCV uses BGR, but MediaPipe uses RGB
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #For performance, image as not writeable while processing
    image_rgb.flags.writeable = False
    results = pose.process(image_rgb)
    image_rgb.flags.writeable = True

    # Convert again to BGR for OpenCV
    output_frame = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    # If pose landmarks are detected, draw them
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            output_frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
        )

    cv2.imshow("MediaPipe Pose - Basic demo", output_frame)

    #Press 'q' to exit
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# 4. Clean up
cap.release()
cap.close()
cv2.destroyAllWindows()