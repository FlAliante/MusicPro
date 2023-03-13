from sqlalchemy import asc, desc
from src.models import Product
from flask import Blueprint, render_template

view_administrador = Blueprint("view_administrador", __name__)


@view_administrador.route("/checkout.html")
def checkout():
    return render_template("demo/checkout.html")


@view_administrador.route("/codes.html")
def codes():
    return render_template("demo/codes.html")


@view_administrador.route("/contact.html")
def contact():
    return render_template("demo/contact.html")


@view_administrador.route("/electronics.html")
def electronics():
    return render_template("demo/electronics.html")


@view_administrador.route("/mens.html")
def mens():
    return render_template("demo/mens.html")


@view_administrador.route("/single.html")
def single():
    return render_template("demo/single.html")


@view_administrador.route("/womens.html")
def womens():
    return render_template("demo/womens.html")
