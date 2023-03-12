from sqlalchemy import asc, desc
from src.models import Product
from flask import Blueprint, render_template

view_cliente = Blueprint("view_cliente", __name__)


@view_cliente.route("/checkout.html")
def checkout():
    return render_template("demo/checkout.html")


@view_cliente.route("/codes.html")
def codes():
    return render_template("demo/codes.html")


@view_cliente.route("/contact.html")
def contact():
    return render_template("demo/contact.html")


@view_cliente.route("/electronics.html")
def electronics():
    return render_template("demo/electronics.html")


@view_cliente.route("/mens.html")
def mens():
    return render_template("demo/mens.html")


@view_cliente.route("/single.html")
def single():
    return render_template("demo/single.html")


@view_cliente.route("/womens.html")
def womens():
    return render_template("demo/womens.html")
