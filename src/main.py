import cv2
import tensorflow as tf
import keras
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask
import pymongo
from processing.thermal_analysis import analyze_thermal_image

def main():
    # Imprimir mensaje de inicialización
    print("Inicializando el análisis térmico de video")
    
    # Ruta de la imagen térmica que se va a analizar
    image_path = "images/thermal_image.jpeg"
    
    # Llamar a la función de análisis térmico y obtener el número de áreas calientes detectadas
    hot_areas = analyze_thermal_image(image_path)
    print(f"Áreas calientes detectadas: {hot_areas}")
    
    # Verificar la carga de la imagen
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is not None:
        # Si la imagen se ha cargado correctamente, imprimir mensaje de éxito
        print("La imagen se ha cargado correctamente.")
    else:
        # Si hay un error al cargar la imagen, imprimir mensaje de error
        print("Error al cargar la imagen.")

# Bloque principal: se ejecuta solo si el script es ejecutado directamente
if __name__ == "__main__":
    main()
