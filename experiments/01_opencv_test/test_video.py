"""
OpenCV video processing test.

Basic test to verify OpenCV functionality for video loading and frame extraction.
"""

import cv2
import os

# Video path (relative to project root)
VIDEO_PATH = os.path.join("data", "raw", "Sentadilla.mp4")

cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("Error: Could not open video file")
    exit(1)

print("Video opened successfully")
print(f"FPS: {cap.get(cv2.CAP_PROP_FPS)}")
print(f"Frame count: {int(cap.get(cv2.CAP_PROP_FRAME_COUNT))}")
print(f"Width: {int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}")
print(f"Height: {int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}")

# Release resources
cap.release()