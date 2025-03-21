from configuracion import PALABRAS_CLAVE_INSECTOS

from configuracion import GOOGLE_VISION_API_KEY


def contiene_insecto(etiquetas):
    """Verifica si las etiquetas de Google Vision contienen un insecto"""
    return any(palabra.lower() in etiqueta.lower() for etiqueta in etiquetas for palabra in PALABRAS_CLAVE_INSECTOS)
