from flask import Blueprint, jsonify, make_response, render_template, request
from config import db_session
import requests

app_controller = Blueprint("view_cliente", __name__)

@app_controller.route("/get_productos", methods=["GET"])
def get_productos():
    
    url = "https://music-pro-api.herokuapp.com/api/get_productos"
    response = requests.get(url)

    serialized_list = []

    if response.status_code == 200:
        for result in response.json():            
            serialized_product = {
                "id": result['código'],
                "description": result['nombre'],
                "photo": result['photo'],
            }
            serialized_list.append(serialized_product)
    else:
        return {"error": f"Hubo un problema al hacer la petición: {response.status_code}"}
    return jsonify(serialized_list)

# Obtener productos por tipo de producto http://localhost:5000/productos/3
@app_controller.route("/get_productos/<tipo_producto>", methods=["GET"])
def get_productos_por_tipo_producto(tipo_producto):

    url = f"https://music-pro-api.herokuapp.com/api/get_productos?tipo_producto={tipo_producto}"
    response = requests.get(url)
    serialized_list = []

    if response.status_code == 200:
        for result in response.json():            
            serialized_product = {
                "id": result['id'],
                "description": result['nombre'],
                "photo": result['photo'],
                "price": result['serie'][0]['valor'],
                "create_time": result['serie'][0]['fecha'],
                "update_time": result['serie'][0]['fecha'],
            }
            serialized_list.append(serialized_product)
    else:
        return {"error": f"Hubo un problema al hacer la petición: {response.status_code}"}
    return jsonify(serialized_list)