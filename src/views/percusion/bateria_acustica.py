from flask import Blueprint, jsonify, make_response, render_template, request
import json
from config import db_session
from sqlalchemy import asc, desc
from src.models import Product


view_bateria_acustica = Blueprint("view_bateria_acustica", __name__)


@view_bateria_acustica.route("/bateria_acustica.html")
def bateria_electronica():
    return render_template("percusion/bateria_acustica.html")