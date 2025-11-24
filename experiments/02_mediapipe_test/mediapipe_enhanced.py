"""
Enhanced MediaPipe Pose experiment.

Adds real-time FPS calculation and shows 7 key landmarks with precision
(visibility) percentage. Highlights landmarks with color coding based on precision.
"""

import time
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
    print(f"Error: Could not open video at {VIDEO_PATH}")
    exit(1)

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)

cv2.namedWindow("MediaPipe Pose - Enhanced", cv2.WINDOW_NORMAL)
cv2.resizeWindow("MediaPipe Pose - Enhanced", 720, 1280)

prev_time = time.time()
fps = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video")
        break

    # Resize to fit screen
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

        keypoints_to_show = [
            mp_pose.PoseLandmark.LEFT_SHOULDER,
            mp_pose.PoseLandmark.LEFT_HIP,
            mp_pose.PoseLandmark.LEFT_KNEE,
            mp_pose.PoseLandmark.LEFT_ANKLE,
            mp_pose.PoseLandmark.RIGHT_HIP,
            mp_pose.PoseLandmark.RIGHT_KNEE,
            mp_pose.PoseLandmark.RIGHT_ANKLE,
        ]

        h_out, w_out = output_frame.shape[:2]

        for kp in keypoints_to_show:
            lm = results.pose_landmarks.landmark[kp]
            cx, cy = int(lm.x * w_out), int(lm.y * h_out)

            visibility = lm.visibility
            precision = visibility * 100  # Convert to percentage

            # Red if visibility < 0.5, yellow if 0.5-0.7, green if > 0.7
            if visibility >= 0.7:
                color = (0, 255, 0)  # Green - high precision
            elif visibility >= 0.5:
                color = (0, 255, 255)  # Yellow - medium precision
            else:
                color = (0, 0, 255)  # Red - low precision

            # Draw larger circle for highlighted points
            cv2.circle(output_frame, (cx, cy), 10, color, -1)
            cv2.circle(output_frame, (cx, cy), 12, color, 2)
            
            # Show point name and precision percentage with background for better visibility
            point_name = kp.name.split('_')[-1]
            precision_text = f"{precision:.1f}%"
            
            # Calculate text position (ensure it's within frame bounds)
            text_x = cx + 15
            text_y1 = cy - 10
            text_y2 = cy + 15
            
            # Ensure text stays within frame
            if text_x > w_out - 100:
                text_x = cx - 100
            if text_y1 < 20:
                text_y1 = cy + 30
            if text_y2 > h_out - 10:
                text_y2 = cy - 10
            
            # Draw solid black background rectangle for text readability
            text_size1 = cv2.getTextSize(point_name, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            text_size2 = cv2.getTextSize(precision_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            max_width = max(text_size1[0], text_size2[0])
            text_height = text_size1[1] + text_size2[1] + 5
            
            # Draw black rectangle background
            cv2.rectangle(
                output_frame,
                (text_x - 5, text_y1 - text_size1[1] - 5),
                (text_x + max_width + 5, text_y2 + 5),
                (0, 0, 0),
                -1
            )
            
            # Draw white border around text box
            cv2.rectangle(
                output_frame,
                (text_x - 5, text_y1 - text_size1[1] - 5),
                (text_x + max_width + 5, text_y2 + 5),
                color,
                2
            )
            
            # Draw text with better visibility - larger font
            cv2.putText(
                output_frame,
                point_name,
                (text_x, text_y1),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),  # White text for better contrast
                2,
            )
            cv2.putText(
                output_frame,
                precision_text,
                (text_x, text_y2),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,  # Colored precision text
                2,
            )
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    cv2.putText(
        output_frame,
        f"FPS: {fps:.1f}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2,
    )

    cv2.imshow("MediaPipe Pose - Enhanced", output_frame)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

