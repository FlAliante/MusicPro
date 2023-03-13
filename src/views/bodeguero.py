from sqlalchemy import asc, desc
from src.models import Product
from flask import Blueprint, render_template

bodeguero_demo = Blueprint("bodeguero_demo", __name__)


@bodeguero_demo.route("/checkout.html")
def checkout():
    return render_template("demo/checkout.html")


@bodeguero_demo.route("/codes.html")
def codes():
    return render_template("demo/codes.html")


@bodeguero_demo.route("/contact.html")
def contact():
    return render_template("demo/contact.html")


@bodeguero_demo.route("/electronics.html")
def electronics():
    return render_template("demo/electronics.html")


@bodeguero_demo.route("/mens.html")
def mens():
    return render_template("demo/mens.html")


@bodeguero_demo.route("/single.html")
def single():
    return render_template("demo/single.html")


@bodeguero_demo.route("/womens.html")
def womens():
    return render_template("demo/womens.html")
