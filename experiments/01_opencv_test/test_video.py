"""
OpenCV video processing test.

Basic test to verify OpenCV functionality for video loading and frame extraction.
"""

from pathlib import Path

import cv2

PROJECT_ROOT = Path(__file__).parent.parent.parent
VIDEO_PATH = PROJECT_ROOT / "data" / "raw" / "Sentadilla.mp4"

cap = cv2.VideoCapture(str(VIDEO_PATH))
if not cap.isOpened():
    print("Error: Could not open video file")
    exit(1)

cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Frame", 480, 800)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Frame", frame)
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
