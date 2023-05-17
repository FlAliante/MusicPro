from flask import Flask, abort
from flask import Blueprint, jsonify, make_response, render_template, request
import json
from config import db_session
from sqlalchemy import asc, desc
from src.models import TipoProducto, Producto
#from .views.producto import view_cliente
import requests

view_producto = Blueprint("view_producto", __name__)

# Api Producto https://music-pro-api.herokuapp.com/productos?tipo_producto=1 -> te devuelve guitarras
@view_producto.route('/productos', methods=['GET'])
def get_productos():
    try:
        tipo_producto = request.args.get("tipo_producto")
        if tipo_producto:
            productos = Producto.query.filter(Producto.tipo_producto == tipo_producto)
        else:
            productos = Producto.query
        serialized_list = []
        for producto in productos:
            serialized_producto = {
                "Serie del producto": "EC-" + str(Producto.random_integer(100, 999)),
                "marca": Producto.random_letters(3),
                "código": f"{Producto.random_letters(3)}-{Producto.random_integer(1000, 9999)}",
                "id": producto.id,
                "nombre": producto.nombre,
                "photo": producto.photo,
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


@view_producto.route('/producto', methods=['GET'])
def get_productos_dos():
    try:
        search = request.args.get("tipo_producto")
        if search:
            productos = Producto.query.filter(Producto.tipo_producto.ilike(f'%{search}%'))  
        else:
            Producto.query
        serialized_list = []
        for producto in productos:
            serialized_producto = {
                "Serie del producto": "EC-256",
                "marca": "LTD",
                "código": "LTD-4943",
                "nombre": producto.nombre,
                "serie": [
                    {
                        "fecha": producto.fecha_creacion,
                        "valor": producto.precio
                    }
                ]
            }
            serialized_list.append(serialized_producto)
        return jsonify(serialized_list)

    except Exception as e:
        print(str(e))
        return make_response({'status': 500, 'error': str(e)}, 500)
    finally:
        db_session.close_all()



# Converidor de Moneda https://music-pro-api.herokuapp.com/amount_clp=1000
@view_producto.route('/', methods=['GET'])
@view_producto.route('/tipos_productos', methods=['GET'])
def get_tipos_productos():
    try:
        tipos_productos = TipoProducto.query.all()
        serialized_list = []
        for tipo_producto in tipos_productos:
            serialized_tipo_producto = tipo_producto.to_dict()
            serialized_list.append(serialized_tipo_producto)
        return jsonify(serialized_list)

    except Exception as e:
        print(str(e))
        return make_response({'status': 500, 'error': str(e)}, 500)
    finally:
        db_session.close_all()