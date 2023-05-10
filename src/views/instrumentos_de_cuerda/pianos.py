from flask import Blueprint, jsonify, make_response, render_template, request
import json
from config import db_session
from sqlalchemy import asc, desc
from src.models import Product


view_pianos = Blueprint("view_pianos", __name__)


@view_pianos.route("/pianos.html")
def pianos():
    return render_template("instrumentos_de_cuerda/pianos.html")