from flask import Flask, abort
from flask import Blueprint, jsonify, make_response, render_template, request
import json
from config import db_session
from sqlalchemy import asc, desc
from src.models import TipoProducto, Producto
#from .views.cliente import view_cliente



app = Flask(__name__)
#app.register_blueprint(view_cliente)

@app.route('/', methods=['GET'])
@app.route('/tipos_productos', methods=['GET'])
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


@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        search = request.args.get("search")
        productos = Producto.query.filter(Producto.nombre.ilike(f'%{search}%')) if search else Producto.query
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