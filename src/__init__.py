from flask import Flask, render_template
# from .views.administrador import view_administrador
# from .views.bodeguero import view_bodeguero
from .views.cliente import view_cliente
# from .views.contador import view_contador
from .views.demo import view_demo
# from .views.vendedor import view_vendedor


app = Flask(__name__)

# app.register_blueprint(view_administrador)
# app.register_blueprint(view_bodeguero)
app.register_blueprint(view_cliente)
# app.register_blueprint(view_contador)
app.register_blueprint(view_demo)
# app.register_blueprint(view_vendedor)


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
