# youtube-playlist

Para que tu script funcione correctamente, necesitarás instalar varias dependencias. Aquí te detallo cómo instalarlas en diferentes sistemas operativos:

## 1. Instalación de pip3 (si no lo tienes)

**En Windows:**
Descarga Python desde python.org y durante la instalación, marca la opción "Add Python to PATH"

**En Linux (Ubuntu/Debian):**
`sudo apt install python3-pip`

**En MacOS:**
`brew install python` (se necesita instalar Homebrew)

## 2. Instalación de FFmpeg (requerido para la conversión de audio)

**En Windows:**
Descargarlo desde su página oficial y luego Añade la carpeta bin a tu PATH:

- Busca "Variables de entorno" en el menú Inicio
- Selecciona "Editar las variables de entorno del sistema"
- Haz clic en "Variables de entorno..."
- En "Variables del sistema", busca "Path" y haz clic en "Editar"
- Añade la ruta completa a la carpeta bin de FFmpeg

**En Linux (Ubuntu/Debian):**
`sudo apt install ffmpeg`

**En MacOS:**
`brew install ffmpeg`

## 3. Instalación de las librerías Python necesarias

Para todos los sistemas operativos, en su terminal hacer `pip3 install yt-dlp mutagen`

