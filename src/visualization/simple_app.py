from flask import Flask

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Definir una ruta para el endpoint raíz ('/')
@app.route('/')
def hello():
    # Retornar un mensaje simple cuando se accede a la raíz del sitio
    return 'Hello, World!'

# Ejecutar la aplicación solo si el script es ejecutado directamente
if __name__ == '__main__':
    # Ejecutar la aplicación Flask en el host '0.0.0.0' y el puerto 5001
    app.run(host='0.0.0.0', port=5001)
