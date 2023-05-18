from sqlalchemy import asc, desc
from src.models.models import Product
from flask import Blueprint, render_template

view_demo = Blueprint('view_demo', __name__)

@view_demo.route("/checkout.html")
def checkout():
    return render_template("demo/checkout.html")

@view_demo.route("/codes.html")
def codes():
    return render_template("demo/codes.html")

@view_demo.route("/contact.html")
def contact():
    return render_template("demo/contact.html")

@view_demo.route("/electronics.html")
def electronics():
    return render_template("demo/electronics.html")

@view_demo.route("/mens.html")
def mens():
    return render_template("demo/mens.html")

@view_demo.route("/single.html")
def single():
    return render_template("demo/single.html")

@view_demo.route("/womens.html")
def womens():
    return render_template("demo/womens.html")