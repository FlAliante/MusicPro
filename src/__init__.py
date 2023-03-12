from flask import Flask, render_template
#from src.controller.product import product

#from .NiceAdmin import admin
#from .SailorSite import site

app = Flask(__name__)

#app.register_blueprint(admin)
#app.register_blueprint(site)


@app.route("/checkout.html")
def checkout():
    return render_template("checkout.html")

@app.route("/codes.html")
def codes():
    return render_template("codes.html")

@app.route("/contact.html")
def contact():
    return render_template("contact.html")

@app.route("/electronics.html")
def electronics():
    return render_template("electronics.html")

@app.route("/")
@app.route("/index.html")
def index():
    return render_template("Base/index.html")

@app.route("/mens.html")
def mens():
    return render_template("mens.html")

@app.route("/single.html")
def single():
    return render_template("single.html")

@app.route("/womens.html")
def womens():
    return render_template("womens.html")


""" @app.errorhandler(500)
def page_internal_error(e):
    return render_template("pages-error-404.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("pages-error-404.html") """