from flask import Blueprint, jsonify, make_response, render_template, request
import json
from config import db_session
from sqlalchemy import asc, desc
from src.models import Product
import requests


view_productos = Blueprint("view_cliente", __name__)

@view_productos.route("/get_productos", methods=["GET"])
def get_productos():
    url = "https://music-pro-api.herokuapp.com/productos"
    response = requests.get(url)

    serialized_list = []

    if response.status_code == 200:
        for result in response.json():            
            serialized_product = {
                "id": result['código'],
                "description": result['nombre'],
                "price": result['serie'][0]['valor'],
                "create_time": result['serie'][0]['fecha'],
                "update_time": result['serie'][0]['fecha'],
                "photo": 'static/images/piano.png',
                "url_nintendo": '',
            }
            serialized_list.append(serialized_product)
    else:
        return {"error": f"Hubo un problema al hacer la petición: {response.status_code}"}
    return jsonify(serialized_list)

@view_productos.route("/list_products", methods=["GET"])
def table_data():
    try:
        search = request.args.get("search")
        sort = request.args.get("sort")
        sort = "price"
        limit = request.args.get("limit")
        offset = request.args.get("offset")

        # obtengo resultados
        total_list = Product.query.filter(Product.description.ilike(f'%{search}%')).count() if search else Product.query.count()
        product_page = Product.query.filter(Product.description.ilike(f'%{search}%')).order_by(Product.price.desc() if sort == 'desc' else Product.price.asc()).offset(int(offset)).limit(int(limit)).all()

        # serializar resultados
        serialized_list = [json.loads(json.dumps(product.to_json())) for product in product_page]

        # armar el objeto json response
        response = {"rows": serialized_list, "total": total_list}
        return jsonify(response)

    except Exception as e:
        print(str(e))
        return make_response(str(e), 500)
    finally:
        # siempre cerrar la sesión, independientemente del resultado
        db_session.close_all()

@view_productos.route("/portfolio/list", methods=["GET"])
def get_table_data():
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