from flask import Flask, request, jsonify
import base64
import os
from procesamiento_imagen import analizar_imagen_google_vision
from clasificacion import contiene_insecto
from informacion_imagen import buscar_info_gemini
from informacion_imagen import buscar_insecto_inaturalist

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "No se envió ninguna imagen"}), 400

    imagen = request.files['image']
    imagen_path = "temp_image.jpg"
    imagen.save(imagen_path)

    # 📌 Analizar la imagen con Google Vision
    resultado = analizar_imagen_google_vision(imagen_path)

    if not resultado:
        return jsonify({"error": "No se pudo analizar la imagen"}), 500

    etiquetas = [e['description'] for e in resultado.get("labelAnnotations", [])]

    if not contiene_insecto(etiquetas):
        return jsonify({"mensaje": "No se encontró ningún insecto en la imagen."})

    nombres_web = [(entity.get('description', ''), entity.get('score', 0))
                   for entity in resultado.get("webDetection", {}).get("webEntities", [])
                   if 'description' in entity and " " in entity['description']]
    nombres_web.sort(key=lambda x: x[1], reverse=True)

    if nombres_web:
        nombre_mas_probable = nombres_web[0][0]
        info = buscar_insecto_inaturalist(nombre_mas_probable)
        info_gemini = buscar_info_gemini(nombre_mas_probable)

        return jsonify({
            "insecto_detectado": True,
            "nombre_comun": info['nombre_comun'],
            "nombre_cientifico": info['nombre_cientifico'],
            "descripcion": info_gemini,
            "imagen": info['imagen'],
            "url_info": info['url_info']
        })

    return jsonify({"error": "No se encontraron coincidencias."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
