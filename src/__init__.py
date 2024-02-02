#Utilizamos Flask
from flask import Flask
#Vistas
from src.views.view import app_view
#Controlador
from src.controllers.controller import app_controller
from src.controllers.api import api_producto

from flask_cors import CORS

app = Flask(__name__)

#Importamos BluePrint
app.register_blueprint(app_view)
app.register_blueprint(app_controller)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.register_blueprint(api_producto)