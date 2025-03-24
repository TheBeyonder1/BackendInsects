import requests
import google.generativeai as genai
from app.services.configuracion import GEMINI_API_KEY

# Configurar la API de Gemini
genai.configure(api_key=GEMINI_API_KEY)


def buscar_info_gemini(nombre_cientifico):
    """Usa Gemini API para obtener información detallada sobre un insecto."""
    
    prompt = f"""
    Dame información sobre el insecto {nombre_cientifico}.
    Quiero saber:
    - Una descripcion Breve.
    - Su hábitat.
    - Su dieta.
    - Su ciclo de vida.
    - Su estado de conservación.
    Responde de forma estructurada y concisa.
    """

    model = genai.GenerativeModel("gemini-2.0-flash-lite")
    response = model.generate_content(prompt)

    if response and hasattr(response, "text"):
        return response.text
    else:
        return "No se pudo obtener información."


def buscar_descripcion_wikipedia(nombre_cientifico):
    """Busca información en Wikipedia sobre el insecto"""
    url = f"https://es.wikipedia.org/api/rest_v1/page/summary/{nombre_cientifico.replace(' ', '_')}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get("extract", "No hay descripción disponible.")
    
    return "No hay descripción disponible."

def buscar_insecto_inaturalist(nombre_insecto):
    url = "https://api.inaturalist.org/v1/taxa"
    params = {
        "q": nombre_insecto,
        "rank": "species",
        "taxon_id": 47158,  # Solo buscar insectos
        "per_page": 1
    }

    response = requests.get(url, params=params)

    if response.status_code == 200 and response.json()["results"]:
        taxon = response.json()["results"][0]
        nombre_cientifico = taxon["name"]

        info = {
            "nombre_comun": taxon.get("preferred_common_name", "Desconocido"),
            "nombre_cientifico": nombre_cientifico,
            "descripcion": taxon.get("wikipedia_summary", "No hay descripción disponible."),
            "imagen": taxon["default_photo"]["medium_url"] if "default_photo" in taxon else "No disponible",
            "url_info": f"https://www.inaturalist.org/taxa/{taxon['id']}",
            "estado_conservacion": taxon.get("conservation_status", {}).get("status", "Desconocido"),
            "habitat": taxon.get("habitat", "Información no disponible"),
            "dieta": taxon.get("diet", "Información no disponible"),
            "ciclo_vida": taxon.get("life_cycle", "Información no disponible")
        }
        return info



    return None
