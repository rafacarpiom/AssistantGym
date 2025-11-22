# AssistantGym

AssistantGym es un sistema de análisis de ejercicios de gimnasio basado en **Pose Estimation**, desarrollado como Trabajo de Fin de Grado.

El objetivo es identificar, evaluar y contar repeticiones de ejercicios mediante modelos de visión por computador, comparando distintos enfoques y construyendo un dataset propio para entrenamiento.

---

## 🧠 Objetivos del proyecto

- Comparar los modelos de pose estimation:
  - **MediaPipe**
  - **MoveNet**
  - **YOLO11 Pose**
- Crear un **dataset propio** de ejercicios reales (sentadillas, press, etc.)
- Diseñar un pipeline de preprocesado:
  - Extracción de frames
  - Normalización de puntos
  - División en fases de movimiento
- Implementar un sistema capaz de:
  - Detectar el ejercicio
  - Contar repeticiones
  - Evaluar técnica
- Documentar los experimentos para justificar la elección del modelo final.

---

## 📂 Estructura del proyecto

AssistantGym/
│
├── venv/ # entorno virtual (siempre oculto en Git)
│
├── src/ # código principal
│ ├── main.py # punto de entrada del proyecto FINAL
│ │
│ ├── pose_estimators/ # implementaciones de los modelos
│ │ ├── mediapipe_pose.py
│ │ ├── movenet_pose.py
│ │ └── yolo11_pose.py
│ │
│ ├── utils/ # funciones auxiliares
│ │ ├── video_utils.py
│ │ ├── angle_utils.py
│ │ └── drawing_utils.py
│ │
│ └── data_pipeline/ # preprocesamiento de datos
│ ├── frame_extractor.py
│ ├── keypoint_processor.py
│ └── dataset_builder.py
│
├── experiments/ # experimentos aislados
│ ├── 01_opencv_test/
│ │ └── test_video.py
│ ├── 02_mediapipe_test/
│ ├── 03_movenet_test/
│ ├── 04_yolo11_test/
│ └── 05_dataset_processing/
│
├── data/ # nunca sube a GitHub
│ ├── raw/ # vídeos originales
│ ├── interim/ # frames, keypoints
│ └── processed/ # dataset final
│
├── results/
│
├── docs/
│ ├── diario_experimentos.md
│ ├── metodologia.md
│ └── arquitectura.md
│
├── .gitignore
└── README.md

---

## 🛠 Tecnologías utilizadas

- **Python 3.11**
- **OpenCV**
- **MediaPipe**
- **MoveNet / TensorFlow**
- **YOLO11 Pose (Ultralytics)**
- **Numpy**
- **Matplotlib**
- **Git + GitHub**
- **Cursor (VSCode-based editor)**

---

## 🧪 Proceso de experimentación

Todos los experimentos se guardan en la carpeta `experiments/`.  
Cada experimento incluye:

- Código independiente
- Resultados guardados en `results/`
- Notas en `docs/diario_experimentos.md`

Esto asegura trazabilidad y justificación para la defensa del TFG.

---

## 🚀 Estado actual

- ✔ Estructura profesional del proyecto creada
- ✔ Entorno virtual configurado
- ⏳ Instalación de modelos de pose estimation
- ⏳ Primeros experimentos en desarrollo

---

## 📌 Autor

**Rafael Carpio Muñoz**  
Grado en Ingeniería Informática  
Universidad de XXXXX
