# Git Cheatsheet Profesional (AssistantGym)

Esta guía recoge **todo lo que necesitas saber** para usar Git de forma profesional dentro del proyecto AssistantGym. Incluye comandos esenciales, reglas de oro, flujo de trabajo recomendado y los pasos que debes seguir cada vez que trabajes en una funcionalidad.

---

PARA PONER ENTORNO VIRTUAL
.\venv\Scripts\activate

## 🟥 1. Los 10 comandos esenciales de Git

### 📌 Inicializar repositorio

```
git init
```

### 📌 Ver el estado del repositorio

```
git status
```

### 📌 Añadir archivos al staging

```
git add .
```

### 📌 Hacer commit con mensaje

```
git commit -m "mensaje claro"
```

### 📌 Ver historial simplificado

```
git log --oneline
```

### 📌 Crear nueva rama

```
git checkout -b nombre-rama
```

### 📌 Cambiar de rama

```
git checkout main
```

### 📌 Fusionar rama con main

```
git merge nombre-rama
```

### 📌 Subir cambios a GitHub

```
git push origin main
```

### 📌 Descargar cambios del remoto

```
git pull
```

---

## 🟩 2. Las 10 reglas de oro de Git

### ⭐ 1. Haz commits pequeños y frecuentes

No guardes miles de líneas de golpe.

### ⭐ 2. Mensajes claros y explicativos

Ejemplo bueno:

```
"Add first MediaPipe inference test with keypoint draw"
```

Ejemplo malo:

```
"arreglos"
```

### ⭐ 3. Una rama por funcionalidad

Ejemplos en AssistantGym:

- `mediapipe-experiments`
- `movenet-experiments`
- `yolo11-experiments`

### ⭐ 4. Jamás trabajes directamente en `main`

`main` siempre debe estar **estable**.

### ⭐ 5. Usa Pull Requests aunque trabajes solo

Da trazabilidad profesional.

### ⭐ 6. No subas archivos grandes

Vídeos, datasets, venv → NO.

### ⭐ 7. Usa siempre `.gitignore`

Evita subir basura al repositorio.

### ⭐ 8. Borras una rama solo si ya está fusionada

Así no pierdes trabajo.

### ⭐ 9. Documenta cambios importantes

Usa `docs/diario_experimentos.md`.

### ⭐ 10. Sin miedo: Git siempre guarda el historial

Puedes volver atrás cuando quieras.

---

## 🟦 3. Flujo de trabajo profesional recomendado

Este es el workflow oficial sugerido para AssistantGym.

### 🔵 Rama principal

```
main
```

Código estable.

---

### 🟣 Ramas de investigación por modelo

```
mediapipe-experiments
movenet-experiments
yolo11-experiments
dataset-tools
app-final
```

---

## 🔥 Flujo para cada funcionalidad

### 1) Crear la rama

```
git checkout -b nombre-rama
```

Ejemplo:

```
git checkout -b mediapipe-experiments
```

### 2) Trabajar y hacer commits pequeños

```
git commit -m "Add initial MediaPipe pose test"
git commit -m "Improve keypoint normalization"
```

### 3) Documentar en docs/diario_experimentos.md

Describe:

- qué probaste
- resultados
- conclusiones

### 4) Subir la rama a GitHub (opcional pero recomendado)

```
git push origin mediapipe-experiments
```

### 5) Crear Pull Request en GitHub

Da trazabilidad profesional.

### 6) Fusionar a main

```
git checkout main
git merge mediapipe-experiments
```

### 7) Borrar la rama (opcional)

```
git branch -d mediapipe-experiments
```

No se pierde nada porque ya está todo en main.

---

## 🟩 5. Resumen profesional

- Git es tu máquina del tiempo.
- Usa ramas para investigar modelos (MediaPipe, MoveNet, YOLO11).
- Main siempre estable.
- Pull Requests = trazabilidad profesional.
- Nunca pierdes historial si subes las ramas a GitHub.
- La documentación del proceso es tan importante como el código.

---
