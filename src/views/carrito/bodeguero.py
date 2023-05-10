from sqlalchemy import asc, desc
from src.models import Product
from flask import Blueprint, render_template

view_bodeguero = Blueprint("bodeguero_demo", __name__)


@view_bodeguero.route("/inventario.html")
def checkout():
    return render_template("bodeguero/inventario.html")