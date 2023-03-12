from flask import Flask, render_template
from .views.demo import view_demo

app = Flask(__name__)

app.register_blueprint(view_demo)

@app.route("/guitarras.html")
def guitarra():
    return render_template("cliente/guitarras.html")

@app.route("/")
@app.route("/index.html")
def index():
    return render_template("index.html")

""" @app.errorhandler(500)
def page_internal_error(e):
    return render_template("pages-error-404.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("pages-error-404.html") """