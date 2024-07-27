import pymongo
import gridfs
from bson import ObjectId

def listar_videos(db_name='thermal_videos', collection_name='videos'):
    # Conectar a MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client[db_name]
    fs = gridfs.GridFS(db, collection=collection_name)

    # Listar todos los videos en la colección
    for file in fs.find():
        print(f"ID: {file._id}, Nombre: {file.filename}, Fecha de subida: {file.uploadDate}")

if __name__ == "__main__":
    listar_videos()
