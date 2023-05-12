from flask import Blueprint, jsonify, make_response, render_template, request
import json
from config import db_session
from sqlalchemy import asc, desc
from src.models import Product

view_carrito = Blueprint("view_carrito", __name__)


@view_carrito.route("/checkout.html")
def checkout():
    return render_template("carrito/checkout.html")