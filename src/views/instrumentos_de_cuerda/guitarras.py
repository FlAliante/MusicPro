from flask import Blueprint, jsonify, make_response, render_template, request
import json
from config import db_session
from sqlalchemy import asc, desc
from src.models import Product


view_guitarras = Blueprint("view_guitarras", __name__)


@view_guitarras.route("/guitarras.html")
def guitarras():
    return render_template("instrumentos_de_cuerda/guitarras.html")