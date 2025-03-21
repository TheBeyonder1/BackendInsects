GOOGLE_VISION_API_KEY = ("AIzaSyCPYX05yDBhq2xgO_lMGbYTv7yufWUQyjY")  # API Key de Google Vision
GEMINI_API_KEY = ("AIzaSyCt0kw894b6kIIcviUCViKEOq8rcgeyKyg")  # API Key de Google AI Studio (Gemini)

if not GOOGLE_VISION_API_KEY or not GEMINI_API_KEY:
    raise ValueError("⚠ ERROR: Falta configurar las API Keys en variables de entorno.")

PALABRAS_CLAVE_INSECTOS = [
    "Insect", "Bug", "Beetle", "Butterfly", "Ant", "Fly", "Grasshopper",
    "Moth", "Caterpillar", "Cockroach", "Dragonfly", "Bee", "Wasp", "Termite"
]