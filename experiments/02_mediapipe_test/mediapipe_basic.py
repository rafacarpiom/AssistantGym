"""
Basic MediaPipe Pose experiment.

Opens a video with OpenCV, runs MediaPipe Pose on each frame,
and draws pose landmarks.
"""

from pathlib import Path

import cv2
import mediapipe as mp

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
VIDEO_PATH = PROJECT_ROOT / "data" / "raw" / "Sentadilla.mp4"

if not VIDEO_PATH.exists():
    print(f"Error: Video file not found at {VIDEO_PATH}")
    exit(1)

cap = cv2.VideoCapture(str(VIDEO_PATH))
if not cap.isOpened():
    print(f"Error: Could not open video file at {VIDEO_PATH}")
    exit(1)

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

cv2.namedWindow("MediaPipe Pose - Basic demo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("MediaPipe Pose - Basic demo", 720, 1280)

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video")
        break

    h, w = frame.shape[:2]
    max_display_width = 720
    if w > max_display_width:
        scale = max_display_width / w
        frame = cv2.resize(frame, (max_display_width, int(h * scale)))

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_rgb.flags.writeable = False
    results = pose.process(image_rgb)
    image_rgb.flags.writeable = True

    output_frame = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            output_frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
        )

    cv2.imshow("MediaPipe Pose - Basic demo", output_frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()