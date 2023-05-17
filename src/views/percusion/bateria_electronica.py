from flask import Blueprint, jsonify, make_response, render_template, request
import json
from config import db_session
from sqlalchemy import asc, desc
from src.models import Product


view_bateria_electronica = Blueprint("view_bateria_electronica", __name__)


@view_bateria_electronica.route("/bateria_electronica.html")
def bateria_electronica():
    return render_template("percusion/bateria_electronica.html")