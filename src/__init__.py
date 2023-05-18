#Utilizamos Flask
from flask import Flask
#demo template
from src.views.demo import view_demo
#Vistas
from src.views.view import app_view
#Controlador
from src.controllers.controller import app_controller


app = Flask(__name__)


#Importamos BluePrint
app.register_blueprint(view_demo)
app.register_blueprint(app_view)
app.register_blueprint(app_controller)