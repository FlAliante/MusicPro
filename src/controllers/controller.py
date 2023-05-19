from flask import Blueprint, jsonify, make_response, request
from sqlalchemy.sql.expression import func

from config import db_session
from src.models.model import Producto

import requests
import locale

api_producto = Blueprint("api_producto", __name__)

# Api Producto https://music-pro-api.herokuapp.com/api/productos?tipo_producto=1 -> te devuelve guitarras
@api_producto.route('/api/get_productos', methods=['GET'])
def get_productos():
    try:
        # Establece el idioma y la ubicación para el formato
        locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')

        #Obtengo variables cargadas en la URL
        tipo_producto = request.args.get("tipo_producto")
        if tipo_producto:
            productos = Producto.query.filter(Producto.tipo_producto == tipo_producto)
        else:
            #Obtengo 10 datos falsos
            productos = Producto.query.order_by(func.random()).limit(10).all()

        #Creo una lista para guardar los productos
        serialized_list = []
        for producto in productos:
            serialized_producto = {
                "Serie del producto": "EC-" + str(Producto.random_integer(100, 999)),
                "codigo": f"{Producto.random_letters(3)}-{Producto.random_integer(1000, 9999)}",
                "marca": producto.marca.strip(),
                "id": producto.id,
                "id_tipo_producto": producto.tipo_producto,
                "nombre": producto.nombre,
                "photo": producto.photo,
                "precio": producto.precio,
                "format_clp": locale.currency(producto.precio, grouping=True, symbol='CLP'),         
                "fecha_actualizacion": producto.fecha_actualizacion,
                "fecha_creacion": producto.fecha_creacion,
                "serie": [
                    {
                        "fecha": producto.fecha_creacion,
                        "valor": producto.precio
                    }
                ],
            }
            serialized_list.append(serialized_producto)
        return jsonify(serialized_list)
    except Exception as e:
        print(str(e))
        return make_response({'status': 500, 'error': str(e)}, 500)
    finally:
        db_session.close_all()


# Converidor de Moneda https://music-pro-api.herokuapp.com/api/exchange_rate?amount_clp=1000
@api_producto.route('/api/exchange_rate', methods=['GET'])
def exchange_rate():
    try:
        amount_clp  = request.args.get("amount_clp")
        if amount_clp :
            url = f'https://v6.exchangerate-api.com/v6/534569873736672ef33d04ea/pair/CLP/USD/{amount_clp}'
        else:
            msj = {
                'status': 500, 
                'error': 'Debes ingresar el monto (amount_clp) para transformarlo a dolar. Example https://music-pro-api.herokuapp.com/amount_clp=1000'
            }
            return make_response(msj,  500)
        response = requests.get(url)
        data = response.json()
        
        # Establece el idioma y la ubicación para el formato
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

        # Formatea el precio con separadores de miles y símbolo de dólar USD
        serialized = {
            "result": data['conversion_result'],
            "format": locale.currency(data['conversion_result'], grouping=True, symbol='USD'),
        }
        return jsonify(serialized)
    except Exception as e:
        print(str(e))
        return make_response({'status': 500, 'error': str(e)}, 500)