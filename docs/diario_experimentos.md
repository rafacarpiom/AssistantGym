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
