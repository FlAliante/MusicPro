from flask import Flask, render_template
#instrumentos_de_cuerda
from .views.instrumentos_de_cuerda.bajos import view_bajos
from .views.instrumentos_de_cuerda.guitarras import view_guitarras
from .views.instrumentos_de_cuerda.pianos import view_pianos

from .views.web_page.productos import view_productos
#from .views.percusión import bateria_acustica, bateria_electronica


app = Flask(__name__)

#instrumentos_de_cuerda
app.register_blueprint(view_bajos)
app.register_blueprint(view_guitarras)
app.register_blueprint(view_pianos)

#percusión
#app.register_blueprint(bateria_acustica)
#app.register_blueprint(bateria_electronica)

app.register_blueprint(view_productos)


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
