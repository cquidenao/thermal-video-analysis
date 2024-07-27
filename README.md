
# Proyecto de Análisis Térmico y Grabación de Video

Este proyecto permite grabar videos desde una cámara Dahua y almacenarlos en MongoDB. También incluye funcionalidades para procesar los videos y analizar imágenes térmicas.


# Renombra este archivo a config.py y rellena los valores apropiados

CAMERA_URL = "rtsp://usuario:contraseña@ip_de_la_camara:puerto/cam/realmonitor?channel=1&subtype=0"
MONGO_URI = "mongodb://usuario:contraseña@localhost:27017/"

### Requisitos

- Python 3.x
- OpenCV
- PyMongo
- GridFS

### Instalación

1. Clona el repositorio:

```sh
git clone https://github.com/tu_usuario/tu_repositorio.git
cd tu_repositorio

### Crea un entorno virtual y actívalo:
python -m venv env
source env/bin/activate  # En Windows usa `env\Scripts\activate`

### Instala las dependencias
pip install -r requirements.txt

### Grabar Video
python grabar_video.py

## Procesar Video
python procesar_video.py --video_id <video_id>
