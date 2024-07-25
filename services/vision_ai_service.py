import os
from google.cloud import vision

def procesar_imagen(image_url):
    """Procesa una imagen de comida con Google Vision AI y devuelve los alimentos identificados con sus respectivas cantidades estimadas."""

    # Configurar el cliente de Google Vision
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    client = vision.ImageAnnotatorClient()

    # Cargar la imagen desde la URL
    image = vision.Image()
    image.source.image_uri = image_url

    # Realizar la detección de etiquetas (label detection)
    response = client.label_detection(image=image)

    # Crear una lista para almacenar los alimentos identificados y sus cantidades (aproximadas)
    alimentos_identificados = []

    for label in response.label_annotations:
        # Filtrar solo etiquetas relevantes a alimentos (puedes personalizar esta lista)
        if label.description.lower() in ["food", "comida", "alimento", "fruit", "fruta", "vegetable", "vegetal", "meat", "carne"]:
            # Estimar la cantidad (esto es un ejemplo básico, puedes mejorarlo con IA)
            cantidad_estimada = 100  # Asumir 100 gramos por defecto (puedes ajustar esto)
            alimentos_identificados.append({
                "nombre": label.description,
                "cantidad": cantidad_estimada
            })

    return alimentos_identificados
