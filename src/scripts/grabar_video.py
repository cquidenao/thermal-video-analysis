import cv2
import datetime
import pymongo
import gridfs
import os
from config import CAMERA_URL, MONGO_URI

def grabar_video(camera_url, duration, db_name='thermal_videos', collection_name='videos'):
    # Conectar a MongoDB usando MONGO_URI
    client = pymongo.MongoClient(MONGO_URI)
    db = client[db_name]
    fs = gridfs.GridFS(db, collection=collection_name)

    # Conectar a la cámara
    cap = cv2.VideoCapture(camera_url)
    if not cap.isOpened():
        print("No se puede abrir la cámara")
        return

    # Obtener las dimensiones del video
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Crear un archivo temporal para guardar el video
    temp_filename = 'temp_video.mp4'
    out = cv2.VideoWriter(temp_filename, fourcc, 20.0, (frame_width, frame_height))

    # Grabar el video durante la duración especificada
    start_time = datetime.datetime.now()
    while (datetime.datetime.now() - start_time).seconds < duration:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    # Liberar los recursos de la cámara
    cap.release()
    out.release()

    # Guardar el video en MongoDB
    with open(temp_filename, 'rb') as f:
        video_id = fs.put(f, filename=temp_filename, uploadDate=datetime.datetime.utcnow())

    print(f"Video guardado en MongoDB con ID: {video_id}")

if __name__ == "__main__":
    duration = 10  # Duración en segundos
    grabar_video(CAMERA_URL, duration)
