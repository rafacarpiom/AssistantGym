"""
MediaPipe Pose – Final experiment script for TFG.

Features:
- Manual parameters at the top of the file
- Fixed model configuration (no runtime changes)
- Save keypoints to CSV (optional)
- Save selected frames on key press (F)
- Display selected landmarks with short labels
- Professional and deterministic setup
"""

import cv2
import csv
import time
from pathlib import Path
import mediapipe as mp


# ============================================================
# 1. MANUAL PARAMETERS (EDIT THESE BEFORE RUNNING)
# ============================================================

MODEL_COMPLEXITY = 2         # 0, 1, 2
MIN_DET_CONF = 0.50
MIN_TRACK_CONF = 0.50
SAVE_KEYPOINTS = True        # True = generate CSV
SAVE_FRAMES = True           # True = allow saving frames with 'F'

VIDEO_NAME = "Sentadilla.mp4"
# ============================================================


# ------------------ Paths ------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
VIDEO_PATH = PROJECT_ROOT / "data" / "raw" / VIDEO_NAME

RESULTS_DIR = PROJECT_ROOT / "results" / "mediapipe"
FRAMES_DIR = RESULTS_DIR / "frames"
KEYPOINTS_DIR = RESULTS_DIR / "keypoints"

FRAMES_DIR.mkdir(parents=True, exist_ok=True)
KEYPOINTS_DIR.mkdir(parents=True, exist_ok=True)


# ------------------ Validate video ------------------
if not VIDEO_PATH.exists():
    print(f"Error: Video file not found at {VIDEO_PATH}")
    exit(1)

cap = cv2.VideoCapture(str(VIDEO_PATH))
if not cap.isOpened():
    print(f"Error: Could not open video file at {VIDEO_PATH}")
    exit(1)


# ------------------ CSV Setup ------------------
csv_writer = None
csv_file = None

if SAVE_KEYPOINTS:
    csv_filename = f"{VIDEO_PATH.stem}_c{MODEL_COMPLEXITY}_d{int(MIN_DET_CONF*100)}_t{int(MIN_TRACK_CONF*100)}.csv"
    csv_path = KEYPOINTS_DIR / csv_filename

    csv_file = open(csv_path, "w", newline="", encoding="utf-8")
    csv_writer = csv.writer(csv_file)

    csv_writer.writerow(["frame", "keypoint", "x", "y", "z", "visibility"])


# ------------------ MediaPipe Setup ------------------
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


# ------------------ Keypoints to track ------------------
TRACKED_KPTS = {
    "SH": mp_pose.PoseLandmark.LEFT_SHOULDER,
    "HIP": mp_pose.PoseLandmark.LEFT_HIP,
    "KN": mp_pose.PoseLandmark.LEFT_KNEE,
    "ANK": mp_pose.PoseLandmark.LEFT_ANKLE,
    "HL": mp_pose.PoseLandmark.LEFT_HEEL,
    "FT": mp_pose.PoseLandmark.LEFT_FOOT_INDEX,
}

# ---- DRAW LANDMARKS + VISIBILITY ---------------------------------------
# Define the subset of keypoints to display
KEYPOINTS_TO_SHOW = {
    "SHOULDER": mp_pose.PoseLandmark.LEFT_SHOULDER,
    "HIP": mp_pose.PoseLandmark.LEFT_HIP,
    "KNEE": mp_pose.PoseLandmark.LEFT_KNEE,
    "ANKLE": mp_pose.PoseLandmark.LEFT_ANKLE,
    "HEEL": mp_pose.PoseLandmark.LEFT_HEEL,
    "FOOT": mp_pose.PoseLandmark.LEFT_FOOT_INDEX,
}


# ------------------ UI Window ------------------
cv2.namedWindow("MediaPipe Pose - Final", cv2.WINDOW_NORMAL)
cv2.resizeWindow("MediaPipe Pose - Final", 720, 1280)


# ============================================================
# 2. MAIN LOOP
# ============================================================

frame_id = 0
paused = False
prev_time = time.time()

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

        # ---- DRAW LANDMARKS + VISIBILITY ---------------------------------------
        if results.pose_landmarks:
            # Draw the skeleton using the default MediaPipe style
            mp_drawing.draw_landmarks(
                output,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_styles.get_default_pose_landmarks_style(),
            )

            # Draw visibility info for each keypoint
            h_img, w_img = output.shape[:2]
            for name, kp in KEYPOINTS_TO_SHOW.items():
                lm = results.pose_landmarks.landmark[kp]
                # Convert normalized coordinates to pixel space
                cx, cy = int(lm.x * w_img), int(lm.y * h_img)
                vis = lm.visibility

                # Choose color based on visibility
                if vis > 0.9:
                    color = (0, 255, 0)   # green
                elif vis > 0.7:
                    color = (0, 255, 255) # yellow
                else:
                    color = (0, 0, 255)   # red

                # Small circle for the point
                cv2.circle(output, (cx, cy), 5, color, -1)

                # Text next to the point
                cv2.putText(
                    output,
                    f"{name}: {vis:.2f}",
                    (cx + 10, cy - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    color,
                    2,
                )

                # Save keypoints to CSV if enabled
                if SAVE_KEYPOINTS:
                    csv_writer.writerow([
                        frame_id, name, lm.x, lm.y, lm.z, lm.visibility
                    ])

    # ------------------ Show output ------------------
    cv2.imshow("MediaPipe Pose - Final", output)

    # ------------------ Keyboard controls ------------------
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    elif key == ord(' '):  # Spacebar
        paused = not paused

    elif key == ord('f') and SAVE_FRAMES:
        frame_name = f"{VIDEO_PATH.stem}_c{MODEL_COMPLEXITY}_d{int(MIN_DET_CONF*100)}_t{int(MIN_TRACK_CONF*100)}_frame_{frame_id}.png"
        cv2.imwrite(str(FRAMES_DIR / frame_name), output)
        print(f"[Saved] {frame_name}")


# ============================================================
# 3. CLEANUP
# ============================================================

cap.release()
cv2.destroyAllWindows()

if csv_file:
    csv_file.close()
    print(f"CSV saved at: {csv_path}")
