import base64
import requests
from app.services.configuracion import GOOGLE_VISION_API_KEY

def cargar_imagen_base64(imagen_path):
    """Codifica una imagen en formato base64"""
    with open(imagen_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def analizar_imagen_google_vision(imagen_path):
    """Envía la imagen a Google Vision API para detectar insectos"""
    encoded_image = cargar_imagen_base64(imagen_path)

    url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_VISION_API_KEY}"
    payload = {
        "requests": [{
            "image": {"content": encoded_image},
            "features": [
                {"type": "LABEL_DETECTION"},
                {"type": "OBJECT_LOCALIZATION"},
                {"type": "WEB_DETECTION"}
            ]
        }]
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()["responses"][0]
    else:
        print("⚠ Error en la solicitud a Google Vision:", response.text)
        return None
