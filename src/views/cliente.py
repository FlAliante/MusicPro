from sqlalchemy import asc, desc
from src.models import Product
from flask import Blueprint, make_response, render_template

view_cliente = Blueprint("view_cliente", __name__)


@view_cliente.route("/guitarras.html")
def guitarras():
    return render_template("cliente/guitarras.html")


@view_cliente.route("/bajos.html")
def bajos():
    return render_template("cliente/bajos.html")


@view_cliente.route("/portfolio/list", methods=["POST"])
def list():
    try:
        my_list = []
        products = Product.query.all()
        total_list = len(products)

        for item in products:
            property = {
                "id": item.id,
                "title": item.description,
                # 'url': item.url,
                "photo": item.photo,
                "price": item.price,
            }
            my_list.append(property)
        return {"rows": my_list, "total": total_list}
    except Exception as e:
        print(str(e))
        return make_response(str(e), 500)
    #finally:
        #return {"rows": my_list, "total": total_list}
