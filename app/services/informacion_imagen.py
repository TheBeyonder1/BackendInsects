import requests
import google.generativeai as genai
from app.services.configuracion import GEMINI_API_KEY

# Configurar la API de Gemini
genai.configure(api_key=GEMINI_API_KEY)


def buscar_info_gemini(nombre_cientifico):
    """Usa Gemini API para obtener información detallada sobre un insecto."""
    
    prompt = f"""
    Proporcióname información detallada sobre el insecto identificado por el nombre científico {nombre_cientifico}.
    La respuesta debe estar organizada en los siguientes campos, con un estilo claro, conciso y profesional:

    Descripción: Redacta un párrafo que describa al insecto de forma fluida y natural, integrando de manera puntual sus características físicas más destacadas, el tamaño promedio y los rasgos distintivos que lo diferencian de otras especies.

    Hábitat: Indica las zonas geográficas donde se encuentra, el tipo de ecosistema que habita (bosques, selvas, desiertos, etc.), y las condiciones ambientales típicas de su entorno.

    Dieta: Explica qué tipo de alimentación tiene (herbívoro, carnívoro, detritívoro, etc.), qué consume habitualmente y cómo obtiene su alimento.

    Ciclo de vida: Describe las etapas del desarrollo del insecto (huevo, larva, pupa, adulto), la duración estimada de cada etapa, y cualquier particularidad sobre su reproducción.

    Estado de conservación: Indica si se encuentra en alguna categoría de amenaza según la UICN (si aplica), cuáles son sus principales amenazas y qué medidas de conservación existen.

    No incluyas frases introductorias ni explicaciones adicionales. Comienza directamente con la información bajo cada título.
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
