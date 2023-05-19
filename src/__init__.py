from flask import Flask
from flask_cors import CORS
from src.controllers.controller import api_producto

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.register_blueprint(api_producto)