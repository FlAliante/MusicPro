from flask import Blueprint, jsonify, make_response, render_template, request
import json
from config import db_session
from sqlalchemy import asc, desc


app_view = Blueprint("app_view", __name__)


#index
""" @app_view.errorhandler(500)
def page_internal_error(e):
    return render_template("pages-error-404.html")

@app_view.errorhandler(404)
def page_not_found(e):
    return render_template("pages-error-404.html") """

@app_view.route("/")
@app_view.route("/index.html")
def index():
    return render_template("index.html")


#instrumentos_de_cuerda
@app_view.route("/bajos.html")
def bajos():
    return render_template("instrumentos_de_cuerda/bajos.html")

@app_view.route("/pianos.html")
def pianos():
    return render_template("instrumentos_de_cuerda/pianos.html")

@app_view.route("/guitarras.html")
def guitarras():
    return render_template("instrumentos_de_cuerda/guitarras.html")


#percusion
@app_view.route("/bateria_electronica.html")
def bateria_electronica():
    return render_template("percusion/bateria_electronica.html")

@app_view.route("/bateria_acustica.html")
def bateria_acustica():
    return render_template("percusion/bateria_acustica.html")


#amplificadores
@app_view.route("/cabezales.html")
def cabezales():
    return render_template("amplificadores/cabezales.html")

@app_view.route("/cajas.html")
def cajas():
    return render_template("amplificadores/cajas.html")


#accesorios
@app_view.route("/audifonos.html")
def audifonos():
    return render_template("accesorios/audifonos.html")

@app_view.route("/monitores.html")
def monitores():
    return render_template("accesorios/monitores.html")

@app_view.route("/parlantes.html")
def parlantes():
    return render_template("accesorios/parlantes.html")

@app_view.route("/cables.html")
def cables():
    return render_template("accesorios/cables.html")

@app_view.route("/microfonos.html")
def microfonos():
    return render_template("accesorios/microfonos.html")

@app_view.route("/interfaces.html")
def interfaces():
    return render_template("accesorios/interfaces.html")

@app_view.route("/mixers.html")
def mixers():
    return render_template("accesorios/mixers.html")

#carrito
@app_view.route("/checkout.html")
def checkout():
    return render_template("carrito/checkout.html")