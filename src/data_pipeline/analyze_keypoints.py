"""
Analyze MediaPipe keypoints CSV and generate a Markdown evaluation report.

Automatically extracts parameters from file name and saves report in:
results/mediapipe/reports/
"""

import argparse
import csv
import re
import statistics
from collections import defaultdict
from pathlib import Path

parser = argparse.ArgumentParser(
    description="Analyze keypoints CSV and generate evaluation report."
)
parser.add_argument(
    "--file",
    type=str,
    required=True,
    help="Path to the CSV file to analyze."
)

args = parser.parse_args()
csv_path = Path(args.file)

if not csv_path.exists():
    print(f"ERROR: File does not exist: {csv_path}")
    exit(1)

print(f"Analyzing file: {csv_path.name}")

match = re.search(r"(.+)_c(\d)_d(\d+)_t(\d+)", csv_path.stem)
if match:
    video_name = match.group(1)
    complexity = match.group(2)
    det_conf = match.group(3)
    track_conf = match.group(4)
else:
    video_name = csv_path.stem
    complexity = "?"
    det_conf = "?"
    track_conf = "?"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

frames_data = defaultdict(list)
keypoint_stats = defaultdict(lambda: {"visibilities": [], "frames_detected": 0})
frame_fps = {}

total_frames = 0
total_detections = 0
has_fps_column = False

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        frame_id = int(row['frame'])
        keypoint = row['keypoint']
        visibility = float(row['visibility'])
        
        if 'fps' in row:
            has_fps_column = True
            if frame_id not in frame_fps:
                fps = float(row['fps'])
                if fps > 0:
                    frame_fps[frame_id] = fps

        total_detections += 1
        keypoint_stats[keypoint]["visibilities"].append(visibility)
        keypoint_stats[keypoint]["frames_detected"] += 1
        frames_data[frame_id].append(visibility)
        total_frames = max(total_frames, frame_id)

lines = []
lines.append(f"# Informe de Evaluación — MediaPipe Pose")
lines.append("")
lines.append(f"**Video:** {video_name}")
lines.append(f"**Model Complexity:** {complexity}")
lines.append(f"**Min Detection Confidence:** {int(det_conf)/100:.2f}")
lines.append(f"**Min Tracking Confidence:** {int(track_conf)/100:.2f}")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 1. Resumen General")
lines.append(f"- Total frames procesados: **{total_frames}**")
lines.append(f"- Total detecciones: **{total_detections}**")
lines.append(f"- Keypoints analizados: **{len(keypoint_stats)}**")
lines.append("")

lines.append("## 2. Estadísticas por Keypoint")
lines.append("")

sorted_keypoints = sorted(
    keypoint_stats.items(),
    key=lambda x: statistics.mean(x[1]["visibilities"]),
    reverse=True
)

for keypoint, stats in sorted_keypoints:
    vis = stats["visibilities"]
    avg_vis = statistics.mean(vis)
    median_vis = statistics.median(vis)
    min_vis = min(vis)
    max_vis = max(vis)
    std_vis = statistics.stdev(vis) if len(vis) > 1 else 0
    coverage = stats["frames_detected"] / total_frames * 100

    lines.append(f"### {keypoint}")
    lines.append(f"- Visibilidad promedio: **{avg_vis*100:.2f}%**")
    lines.append(f"- Mediana: {median_vis:.4f}")
    lines.append(f"- Rango: [{min_vis:.4f}, {max_vis:.4f}]")
    lines.append(f"- Desviación estándar: {std_vis:.4f}")
    lines.append(f"- Cobertura: **{coverage:.2f}%**")
    lines.append("")

all_vis = [v for kp in keypoint_stats.values() for v in kp["visibilities"]]
overall_avg = statistics.mean(all_vis)
overall_median = statistics.median(all_vis)

lines.append("## 3. Calidad General")
lines.append(f"- Visibilidad promedio general: **{overall_avg*100:.2f}%**")
lines.append(f"- Mediana general: {overall_median:.4f}")
lines.append("")

if has_fps_column and frame_fps:
    fps_values = list(frame_fps.values())
    avg_fps = statistics.mean(fps_values)
    median_fps = statistics.median(fps_values)
    min_fps = min(fps_values)
    max_fps = max(fps_values)
    std_fps = statistics.stdev(fps_values) if len(fps_values) > 1 else 0
    
    lines.append("## 4. Rendimiento (FPS)")
    lines.append(f"- FPS promedio: **{avg_fps:.2f}**")
    lines.append(f"- FPS mediano: {median_fps:.2f}")
    lines.append(f"- FPS mínimo: {min_fps:.2f}")
    lines.append(f"- FPS máximo: {max_fps:.2f}")
    lines.append(f"- Desviación estándar: {std_fps:.2f}")
    lines.append("")

REPORTS_DIR = PROJECT_ROOT / "results" / "mediapipe" / "reports" / "mediapipe"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

report_filename = f"{video_name}_c{complexity}_d{det_conf}_t{track_conf}_report.md"
REPORT_PATH = REPORTS_DIR / report_filename

with open(REPORT_PATH, 'w', encoding='utf-8') as f:
    f.write("\n".join(lines))

print(f"\nReport generated successfully:")
print(REPORT_PATH)
