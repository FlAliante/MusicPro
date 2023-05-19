from flask import Blueprint, jsonify, make_response, render_template, request
from config import db_session
import requests

app_controller = Blueprint("view_cliente", __name__)

# Obtener productos por tipo de producto http://localhost:5000/productos/3
@app_controller.route("/get_productos", methods=["GET"])
def get_productos():
    url = "https://music-pro-api.herokuapp.com/api/get_productos"
    try:
        response = requests.get(url)
        response.raise_for_status()
        serialized_list = []

        for result in response.json():
            serialized_product = {
                "id": result['id'],
                "nombre": result['nombre'],
                "photo": result['photo'],
                "precio": result['precio'],
                "format_clp": result['format_clp'],
            }
            serialized_list.append(serialized_product)
        return jsonify(serialized_list)
    
    except Exception as e:
        error = { "status": 500, "error": str(e) }
        print(error)
        return make_response(error, 500)

# Obtener productos por tipo de producto http://localhost:5000/productos/3
@app_controller.route("/get_productos/<tipo_producto>", methods=["GET"])
def get_productos_tipo_producto(tipo_producto):

    url = f"https://music-pro-api.herokuapp.com/api/get_productos?tipo_producto={tipo_producto}"
    response = requests.get(url)
    serialized_list = []

    if response.status_code == 200:
        for result in response.json():            
            serialized_product = {
                "id": result['id'],
                "nombre": result['nombre'],
                "photo": result['photo'],
                "precio": result['precio'],
                "format_clp": result['format_clp'],
            }
            serialized_list.append(serialized_product)
    else:
        return {"error": f"Hubo un problema al hacer la petición: {response.status_code}"}
    return jsonify(serialized_list)