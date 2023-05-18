from flask import Blueprint, jsonify, make_response, render_template, request
import json
from config import db_session
from sqlalchemy import asc, desc


app_view = Blueprint("view_bateria_acustica", __name__)

@app_view.route("/")
@app_view.route("/index.html")
def index():
    return render_template("index.html")

""" @app_view.errorhandler(500)
def page_internal_error(e):
    return render_template("pages-error-404.html")


@app_view.errorhandler(404)
def page_not_found(e):
    return render_template("pages-error-404.html") """

@app_view.route("/bateria_acustica.html")
def bateria_electronica():
    return render_template("instrumentos_de_cuerda/bateria_acustica.html")


@app_view.route("/bateria_acustica.html")
def bateria_electronica():
    return render_template("percusion/bateria_acustica.html")


@app_view.route("/checkout.html")
def checkout():
    return render_template("carrito/checkout.html")