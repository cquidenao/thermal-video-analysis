import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cv2
import pymongo
import gridfs
import numpy as np
from bson import ObjectId
from processing.thermal_analysis import analyze_thermal_image

def procesar_video(video_id, db_name='thermal_videos', collection_name='videos'):
    # Conectar a MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client[db_name]
    fs = gridfs.GridFS(db, collection=collection_name)

    # Convertir el ID del video a ObjectId y obtener el archivo de video
    video_file = fs.get(ObjectId(video_id))
    temp_filename = 'temp_video_to_process.mp4'
    with open(temp_filename, 'wb') as f:
        f.write(video_file.read())

    # Abrir el archivo de video
    cap = cv2.VideoCapture(temp_filename)
    if not cap.isOpened():
        print("No se puede abrir el archivo de video")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Procesar cada frame
        temp_image_path = 'temp_frame.jpg'
        cv2.imwrite(temp_image_path, frame)
        results = analyze_thermal_image(temp_image_path)
        thermal_image = results["image_with_contours"]

        # Mostrar el frame procesado (opcional)
        cv2.imshow('Frame Procesado', thermal_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Reemplaza '66a40244da596075bed698aa' con el ID real del video guardado en MongoDB
    video_id = '66a40244da596075bed698aa'
    procesar_video(video_id)
