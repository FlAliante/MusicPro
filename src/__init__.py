from flask import Flask, abort
from flask import Blueprint, jsonify, make_response, render_template, request
import json
from config import db_session
from sqlalchemy import asc, desc
from src.models import Product
from .views.cliente import view_cliente



app = Flask(__name__)
#app.register_blueprint(view_cliente)

elementos = [
    {
        'id': 1,
        'nombre': 'Elemento 1',
        'descripcion': 'Este es el elemento 1'
    },
    {
        'id': 2,
        'nombre': 'Elemento 2',
        'descripcion': 'Este es el elemento 2'
    }
]

@app.route('/', methods=['GET'])
@app.route('/productos', methods=['GET'])
def get_productos():
    try:
        products = Product.query.all()
        serialized_list = []
        for product in products:
            serialized_product = {
                "id": product.id,
                "description": product.description,
                "create_time": str(product.create_time),
                "update_time": str(product.update_time),
                "price": product.price,
                "photo": product.photo,
                "url_nintendo": product.url_nintendo,
            }

            serialized_list.append(serialized_product)
        return jsonify(serialized_list)

    except Exception as e:
        print(str(e))
        return make_response(str(e), 500)
    finally:
        # siempre cerrar la sesión, independientemente del resultado
        db_session.close_all()

@app.route('/elementos', methods=['GET'])
def obtener_elementos():
    try:
        products = Product.query.all()
        serialized_list = []
        for product in products:
            serialized_product = {
                "id": product.id,
                "description": product.description,
                "create_time": str(product.create_time),
                "update_time": str(product.update_time),
                "price": product.price,
                "photo": product.photo,
                "url_nintendo": product.url_nintendo,
            }

            serialized_list.append(serialized_product)
        return jsonify(serialized_list)

    except Exception as e:
        print(str(e))
        return make_response(str(e), 500)
    finally:
        # siempre cerrar la sesión, independientemente del resultado
        db_session.close_all()


@app.route('/elementos/<int:id>', methods=['GET'])
def obtener_elemento(id):
    elemento = [elemento for elemento in elementos if elemento['id'] == id]
    if len(elemento) == 0:
        abort(404)
    return jsonify({'elemento': elemento[0]})


@app.route('/elementos', methods=['POST'])
def agregar_elemento():
    if not request.json or not 'nombre' in request.json:
        abort(400)
    elemento = {
        'id': elementos[-1]['id'] + 1,
        'nombre': request.json['nombre'],
        'descripcion': request.json.get('descripcion', "")
    }
    elementos.append(elemento)
    return jsonify({'elemento': elemento}), 201


@app.route('/elementos/<int:id>', methods=['PUT'])
def actualizar_elemento(id):
    elemento = [elemento for elemento in elementos if elemento['id'] == id]
    if len(elemento) == 0:
        abort(404)
    if not request.json:
        abort(400)
    elemento[0]['nombre'] = request.json.get('nombre', elemento[0]['nombre'])
    elemento[0]['descripcion'] = request.json.get('descripcion', elemento[0]['descripcion'])
    return jsonify({'elemento': elemento[0]})

@app.route('/elementos/<int:id>', methods=['DELETE'])
def delete_task(id):
    elemento = [elemento for elemento in elementos if elemento['id'] == id]
    if len(elemento) == 0:
        abort(404)
    elementos.remove(elemento[0])
    return jsonify({'result': True})




