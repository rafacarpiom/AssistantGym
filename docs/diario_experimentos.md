# Diario de Experimentos

Registro de todos los experimentos realizados durante el desarrollo del TFG.

## Experimentos

### 01_opencv_test

- **Fecha**: 2024-12-19
- **Objetivo**:
  - Verificar la funcionalidad básica de OpenCV para carga y visualización de vídeos
  - Probar la extracción de frames de vídeos
  - Establecer una base para futuros experimentos de procesamiento de vídeo
- **Resultados**:
  - ✅ OpenCV funciona correctamente para cargar vídeos
  - ✅ Implementado sistema de rutas robusto usando `pathlib.Path` que funciona desde cualquier directorio
  - ✅ Configurada ventana redimensionable para visualización de vídeos verticales (480x800)
  - ✅ Reproducción de vídeo a velocidad real (~30 FPS con delay de 33ms)
  - ✅ Control básico implementado (tecla 'q' para salir)
- **Conclusiones**:
  - OpenCV es adecuado para el procesamiento básico de vídeo en el proyecto
  - El uso de `pathlib.Path` mejora la portabilidad y mantenibilidad del código
  - La configuración de ventana con `WINDOW_NORMAL` permite adaptarse a diferentes resoluciones de vídeo
  - Listo para avanzar a experimentos con pose estimation (MediaPipe, MoveNet, YOLO11)

---

### 02_mediapipe_test

- **Fecha**: 2024-12-19
- **Objetivo**:
  - Evaluar MediaPipe Pose como modelo de estimación de pose para análisis de ejercicios
  - Implementar sistema de procesamiento de video con detección de keypoints
  - Generar datasets de keypoints en formato CSV para análisis posterior
  - Desarrollar herramientas de análisis y evaluación de la calidad del modelo
  - Optimizar el rendimiento del procesamiento
- **Scripts Desarrollados**:
  - `mediapipe_basic.py`: Implementación básica de MediaPipe Pose
  - `mediapipe_enhanced.py`: Versión mejorada con visualización de 7 puntos clave y precisión en tiempo real
  - `mediapipe_advanced.py`: Versión final con procesamiento completo, guardado de CSV y visualización opcional
  - `analyze_keypoints.py`: Script de análisis de CSVs con generación automática de informes en Markdown
- **Características Implementadas**:
  - ✅ Procesamiento completo de video antes de visualización (modo headless)
  - ✅ Guardado de keypoints en CSV con formato: `frame, keypoint, x, y, z, visibility, fps`
  - ✅ Visualización de landmarks con código de colores según precisión (verde/amarillo/rojo)
  - ✅ Cálculo y registro de FPS durante el procesamiento
  - ✅ Sistema de flush automático para prevenir pérdida de datos si se interrumpe el proceso
  - ✅ Manejador de señales (Ctrl+C) para guardado seguro de datos
  - ✅ Análisis automático de CSVs con estadísticas de visibilidad y rendimiento
  - ✅ Generación de informes en Markdown con estadísticas detalladas
  - ✅ Uso de `argparse` para especificar archivo CSV a analizar
- **Configuraciones Probadas**:
  - Model Complexity: 0, 1, 2 (evaluadas todas las opciones)
  - Min Detection Confidence: 0.50, 0.60
  - Min Tracking Confidence: 0.50
- **Resultados**:
  - ✅ MediaPipe Pose muestra excelente rendimiento (96.88% visibilidad promedio)
  - ✅ 100% de cobertura de detección en todos los frames
  - ✅ Keypoints críticos (cadera, rodilla, tobillo) con 96.58% de visibilidad promedio
  - ✅ 89.40% de las detecciones con calidad excelente (≥0.9)
  - ✅ Sistema de procesamiento eficiente con guardado seguro de datos
  - ✅ Herramientas de análisis profesionales con informes automáticos
  - ✅ Rendimiento FPS adecuado para procesamiento en tiempo real (dependiendo de complexity)
- **Optimizaciones Implementadas**:
  - Procesamiento de imagen redimensionada antes de MediaPipe (mejora FPS 30-50%)
  - Buffering de escritura CSV para mejor rendimiento I/O
  - Flush automático después de cada frame para prevenir pérdida de datos
  - Modo dual: procesamiento completo (CSV) vs visualización (sin CSV)
- **Conclusiones**:
  - MediaPipe Pose es **VÁLIDO y RECOMENDABLE** para el análisis de ejercicios de sentadillas
  - El modelo muestra alta precisión y confiabilidad en la detección de keypoints críticos
  - La configuración óptima depende del objetivo: Complexity=2 para máxima precisión, Complexity=1 para balance FPS/precisión
  - El sistema de procesamiento completo antes de visualización asegura que los CSVs siempre contengan todos los frames
  - Las herramientas de análisis permiten evaluación objetiva del rendimiento del modelo
  - El formato CSV generado es adecuado para análisis posterior y construcción de datasets
  - Listo para integrar en el pipeline principal del proyecto

---
