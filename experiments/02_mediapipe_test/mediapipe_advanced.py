"""
MediaPipe Pose experiment script.

Processes video with MediaPipe Pose to extract keypoints and save to CSV.
Can run in headless mode (CSV generation only) or display mode (visualization only).
"""

import csv
import signal
import sys
import time
from pathlib import Path

import cv2
import mediapipe as mp

# Configuration
MODEL_COMPLEXITY = 2
MIN_DET_CONF = 0.50
MIN_TRACK_CONF = 0.50
SAVE_KEYPOINTS = True
SAVE_FRAMES = True
VIDEO_NAME = "Sentadilla.mp4"

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
VIDEO_PATH = PROJECT_ROOT / "data" / "raw" / VIDEO_NAME

RESULTS_DIR = PROJECT_ROOT / "results" / "mediapipe"
FRAMES_DIR = RESULTS_DIR / "frames"
KEYPOINTS_DIR = RESULTS_DIR / "keypoints"

FRAMES_DIR.mkdir(parents=True, exist_ok=True)
KEYPOINTS_DIR.mkdir(parents=True, exist_ok=True)

# Validate video
if not VIDEO_PATH.exists():
    print(f"Error: Video file not found at {VIDEO_PATH}")
    exit(1)

temp_cap = cv2.VideoCapture(str(VIDEO_PATH))
total_frames_video = int(temp_cap.get(cv2.CAP_PROP_FRAME_COUNT))
temp_cap.release()

cap = cv2.VideoCapture(str(VIDEO_PATH))
if not cap.isOpened():
    print(f"Error: Could not open video file at {VIDEO_PATH}")
    exit(1)

# CSV setup
csv_writer = None
csv_file = None
csv_path = None

if SAVE_KEYPOINTS:
    csv_filename = f"{VIDEO_PATH.stem}_c{MODEL_COMPLEXITY}_d{int(MIN_DET_CONF*100)}_t{int(MIN_TRACK_CONF*100)}.csv"
    csv_path = KEYPOINTS_DIR / csv_filename

    csv_file = open(csv_path, "w", newline="", encoding="utf-8")
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(["frame", "keypoint", "x", "y", "z", "visibility", "fps"])
    csv_file.flush()

def signal_handler(sig, frame):
    """Save CSV when process is interrupted."""
    print("\n\nInterruption detected. Saving data...")
    if csv_file:
        csv_file.flush()
        csv_file.close()
        print(f"CSV saved at: {csv_path}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# MediaPipe setup
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=MODEL_COMPLEXITY,
    enable_segmentation=False,
    min_detection_confidence=MIN_DET_CONF,
    min_tracking_confidence=MIN_TRACK_CONF,
)

KEYPOINTS_TO_SHOW = {
    "SHOULDER": mp_pose.PoseLandmark.LEFT_SHOULDER,
    "HIP": mp_pose.PoseLandmark.LEFT_HIP,
    "KNEE": mp_pose.PoseLandmark.LEFT_KNEE,
    "ANKLE": mp_pose.PoseLandmark.LEFT_ANKLE,
    "HEEL": mp_pose.PoseLandmark.LEFT_HEEL,
    "FOOT": mp_pose.PoseLandmark.LEFT_FOOT_INDEX,
}

if not SAVE_KEYPOINTS:
    cv2.namedWindow("MediaPipe Pose - Final", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("MediaPipe Pose - Final", 720, 1280)

frame_id = 0
paused = False
prev_time = time.time()

# Process full video first to generate complete CSV
if SAVE_KEYPOINTS:
    print("=" * 80)
    print("FULL VIDEO PROCESSING")
    print(f"Processing {total_frames_video} frames to generate complete CSV...")
    print("=" * 80)
    
    # Reset video to beginning
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    processing_start = time.time()
    frames_processed = 0
    prev_frame_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_id += 1
        frames_processed += 1
        
        curr_frame_time = time.time()
        frame_fps = 1.0 / (curr_frame_time - prev_frame_time) if (curr_frame_time - prev_frame_time) > 0 else 0.0
        prev_frame_time = curr_frame_time
        
        h, w = frame.shape[:2]
        max_display_width = 720
        if w > max_display_width:
            scale = max_display_width / w
            frame = cv2.resize(frame, (max_display_width, int(h * scale)))
        
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = pose.process(image_rgb)
        image_rgb.flags.writeable = True
        
        if results.pose_landmarks:
            for name, kp in KEYPOINTS_TO_SHOW.items():
                lm = results.pose_landmarks.landmark[kp]
                csv_writer.writerow([
                    frame_id, name, lm.x, lm.y, lm.z, lm.visibility, frame_fps
                ])
        
        csv_file.flush()
        if frame_id % 50 == 0 or frame_id == total_frames_video:
            progress = (frame_id / total_frames_video) * 100
            elapsed = time.time() - processing_start
            fps_processing = frame_id / elapsed if elapsed > 0 else 0
            print(f"Progress: {frame_id}/{total_frames_video} frames ({progress:.1f}%) | "
                  f"FPS: {fps_processing:.1f} | Time: {elapsed:.1f}s")
    
    csv_file.flush()
    processing_time = time.time() - processing_start
    
    print("=" * 80)
    print(f"✓ Processing completed!")
    print(f"  - Frames processed: {frames_processed}")
    print(f"  - Total time: {processing_time:.2f} seconds")
    print(f"  - Average FPS: {frames_processed/processing_time:.2f}")
    print(f"  - CSV saved at: {csv_path}")
    print("=" * 80)
    
    csv_file.close()
    cap.release()
    print("\nProcessing completed. Exiting...")
    exit(0)

# Display loop
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
frame_id = 0

while True:

    if not paused:
        ret, frame = cap.read()
        if not ret:
            print("End of video.")
            break

        frame_id += 1

        h, w = frame.shape[:2]
        max_display_width = 720
        if w > max_display_width:
            scale = max_display_width / w
            frame = cv2.resize(frame, (max_display_width, int(h * scale)))

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_rgb.flags.writeable = False
        results = pose.process(image_rgb)
        image_rgb.flags.writeable = True

        output = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        # FPS calculation
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time

        cv2.putText(output, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                output,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_styles.get_default_pose_landmarks_style(),
            )

            h_img, w_img = output.shape[:2]
            for name, kp in KEYPOINTS_TO_SHOW.items():
                lm = results.pose_landmarks.landmark[kp]
                cx, cy = int(lm.x * w_img), int(lm.y * h_img)
                vis = lm.visibility

                if vis > 0.9:
                    color = (0, 255, 0)
                elif vis > 0.7:
                    color = (0, 255, 255)
                else:
                    color = (0, 0, 255)

                cv2.circle(output, (cx, cy), 5, color, -1)
                cv2.putText(
                    output,
                    f"{name}: {vis:.2f}",
                    (cx + 10, cy - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    2,
                )

    cv2.imshow("MediaPipe Pose - Final", output)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord(' '):
        paused = not paused
    elif key == ord('f') and SAVE_FRAMES:
        frame_name = f"{VIDEO_PATH.stem}_c{MODEL_COMPLEXITY}_d{int(MIN_DET_CONF*100)}_t{int(MIN_TRACK_CONF*100)}_frame_{frame_id}.png"
        cv2.imwrite(str(FRAMES_DIR / frame_name), output)
        print(f"[Saved] {frame_name}")

cap.release()
cv2.destroyAllWindows()
print(f"Video finished. Total frames displayed: {frame_id}")
