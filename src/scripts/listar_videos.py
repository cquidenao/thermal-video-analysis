import pymongo
import gridfs
from bson import ObjectId

def listar_videos(db_name='thermal_videos', collection_name='videos'):
    """
    Función para listar todos los videos almacenados en una colección de GridFS en MongoDB.

    Parámetros:
    db_name (str): Nombre de la base de datos en MongoDB.
    collection_name (str): Nombre de la colección en GridFS.

    Retorno:
    None
    """
    # Conectar a MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client[db_name]
    fs = gridfs.GridFS(db, collection=collection_name)

    # Listar todos los videos en la colección
    for file in fs.find():
        print(f"ID: {file._id}, Nombre: {file.filename}, Fecha de subida: {file.uploadDate}")

if __name__ == "__main__":
    """
    Bloque principal del script.
    Llama a la función listar_videos para mostrar todos los videos en la colección.
    """
    listar_videos()
