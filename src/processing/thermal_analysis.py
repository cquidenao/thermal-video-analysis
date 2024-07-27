import cv2
import numpy as np

def analyze_thermal_image(image_path):
    # Leer la imagen en escala de grises
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("No se pudo cargar la imagen.")

    # Aplicar mapa de color térmico
    thermal_img = cv2.applyColorMap(img, cv2.COLORMAP_JET)

    # Calcular parámetros térmicos
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(img)
    avg_val = np.mean(img)
    std_dev = np.std(img)  # Desviación estándar

    # Rango de temperatura para detectar anomalías
    lower_threshold = 20
    upper_threshold = 25

    # Máscara para identificar áreas fuera del rango de temperatura
    anomaly_mask = cv2.inRange(img, lower_threshold, upper_threshold)
    anomaly_mask = cv2.bitwise_not(anomaly_mask)  # Invertir máscara para áreas fuera del rango
    contours, _ = cv2.findContours(anomaly_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(thermal_img, contours, -1, (0, 0, 255), 2)

    return {
        "min_temp": min_val,  # Temperatura mínima
        "max_temp": max_val,  # Temperatura máxima
        "avg_temp": avg_val,  # Temperatura promedio
        "std_dev": std_dev,  # Desviación estándar
        "lower_threshold": lower_threshold,  # Umbral inferior
        "upper_threshold": upper_threshold,  # Umbral superior
        "anomalies": [(cv2.boundingRect(contour), cv2.contourArea(contour)) for contour in contours],  # Anomalías detectadas
        "image_with_contours": thermal_img  # Imagen con contornos dibujados
    }
