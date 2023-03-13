from sqlalchemy import asc, desc
from src.models import Product
from flask import Blueprint, render_template

view_contador = Blueprint('view_contador', __name__)

@view_contador.route("/checkout.html")
def checkout():
    return render_template("demo/checkout.html")

@view_contador.route("/codes.html")
def codes():
    return render_template("demo/codes.html")

@view_contador.route("/contact.html")
def contact():
    return render_template("demo/contact.html")

@view_contador.route("/electronics.html")
def electronics():
    return render_template("demo/electronics.html")

@view_contador.route("/mens.html")
def mens():
    return render_template("demo/mens.html")

@view_contador.route("/single.html")
def single():
    return render_template("demo/single.html")

@view_contador.route("/womens.html")
def womens():
    return render_template("demo/womens.html")