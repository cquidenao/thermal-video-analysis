import sys
import os
import logging
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

import cv2
import base64
import numpy as np
from flask import Flask, render_template, url_for, send_from_directory, request, redirect
from flask_socketio import SocketIO, emit
import pymongo
import gridfs
import datetime
from bson import ObjectId
from src.processing.thermal_analysis import analyze_thermal_image  # Asegúrate de que esta línea esté correcta

# Crear una instancia de la aplicación Flask
app = Flask(__name__, template_folder="../templates", static_folder="../static")
# Crear una instancia de SocketIO para la aplicación
socketio = SocketIO(app)

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Conexión a MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['thermal_videos']
fs = gridfs.GridFS(db, collection='videos')

# Definir la ruta raíz
@app.route('/')
def index():
    logger.debug("Ruta / invocada")
    return render_template('index.html')

# Ruta para subir imágenes térmicas
@app.route('/upload', methods=['POST'])
def upload_image():
    logger.debug("Ruta /upload invocada")
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        if not os.path.exists(app.static_folder):
            os.makedirs(app.static_folder)
        filepath = os.path.join(app.static_folder, file.filename)
        file.save(filepath)
        try:
            results = analyze_thermal_image(filepath)
            output_path = os.path.join(app.static_folder, 'thermal_output.jpg')
            cv2.imwrite(output_path, results["image_with_contours"])
            return render_template('result.html', results=results, image_url=url_for('static', filename='thermal_output.jpg'))
        except ValueError as e:
            return str(e)

# Ruta para capturar video
@app.route('/capture_video')
def capture_video():
    logger.debug("Ruta /capture_video invocada")
    return render_template('video.html')

# Ruta para grabar video desde una cámara
@app.route('/grabar_video', methods=['POST'])
def grabar_video():
    logger.debug("Ruta /grabar_video invocada")
    camera_url = request.form.get('camera_url')
    duration = int(request.form.get('duration'))

    cap = cv2.VideoCapture(camera_url)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Configurar el tamaño del búfer
    if not cap.isOpened():
        logger.error("No se puede abrir la cámara")
        return "No se puede abrir la cámara"

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    temp_filename = 'temp_video.mp4'
    out = cv2.VideoWriter(temp_filename, fourcc, 20.0, (frame_width, frame_height))

    start_time = datetime.datetime.now()
    while (datetime.datetime.now() - start_time).seconds < duration:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()

    with open(temp_filename, 'rb') as f:
        video_id = fs.put(f, filename=temp_filename, uploadDate=datetime.datetime.utcnow())

    return f"Video guardado en MongoDB con ID: {video_id}"

# Ruta para procesar un video almacenado en MongoDB
@app.route('/procesar_video', methods=['POST'])
def procesar_video():
    logger.debug("Ruta /procesar_video invocada")
    video_id = request.form.get('video_id')

    try:
        video_file = fs.get(ObjectId(video_id))
        temp_filename = 'temp_video_to_process.mp4'
        with open(temp_filename, 'wb') as f:
            f.write(video_file.read())

        cap = cv2.VideoCapture(temp_filename)
        if not cap.isOpened():
            logger.error("No se puede abrir el archivo de video")
            return "No se puede abrir el archivo de video"

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            temp_image_path = 'temp_frame.jpg'
            cv2.imwrite(temp_image_path, frame)
            results = analyze_thermal_image(temp_image_path)
            thermal_image = results["image_with_contours"]

            cv2.imshow('Frame Procesado', thermal_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        return "Video procesado correctamente"
    except Exception as e:
        logger.error(f"Error procesando el video: {str(e)}")
        return str(e)

# Ruta de prueba
@app.route('/test')
def test():
    logger.debug("Ruta /test invocada")
    return "Ruta de prueba funcionando"

# Ruta para mostrar imágenes estáticas
@app.route('/static/<filename>')
def display_image(filename):
    logger.debug(f"Ruta /static/{filename} invocada")
    return send_from_directory(app.static_folder, filename)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Iniciar el servidor Flask")
    parser.add_argument('--port', type=int, default=8082, help='Puerto en el que se ejecutará el servidor')
    args = parser.parse_args()

    logger.debug("Iniciando la aplicación Flask con SocketIO")
    socketio.run(app, host='0.0.0.0', port=args.port)
