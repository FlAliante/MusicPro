from sqlalchemy import asc, desc
from src.models import Product
from flask import Blueprint, render_template


view_bajos = Blueprint("view_bajos", __name__)


@view_bajos.route("/bajos.html")
def bajos():
    return render_template("instrumentos_de_cuerda/bajos.html")