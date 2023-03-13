from . import site
from sqlalchemy import asc, desc
from src.models import Product
from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify, make_response


@site.route('/redirect')
def properaty():
    return redirect(url_for('pages_login'))


@site.route('/portfolio')
def property():
    return render_template('portfolio/portfolio.html')


@site.route('/portfolio/list', methods=['POST'])
def broker_list():
    try:
        my_list = []
        #search = request.form['search']
        tag = request.form["search"]
        search = "%{}%".format(tag)
        sort = request.form['sort']
        limit = request.form['limit']
        offset = request.form['offset']
        order = request.form["order"]
        #query = Product.query
        if order == 'asc':
            products = Product.query.filter(Product.description.ilike(search)).order_by(asc(sort)).offset(offset).limit(limit)
        else:
            products = Product.query.filter(Product.description.ilike(search)).order_by(desc(sort)).offset(offset).limit(limit)
        if tag == '':
            total_list = Product.query.count()
        else:
            total_list = products.count()
        for item in products:
            property = {
                'id': item.id,
                'title': item.description,
                # 'url': item.url,
                'photo': item.photo,
                'price': item.price,
            }
            my_list.append(property)
        return {
            'rows': my_list,
            'total': total_list
        }
    except Exception as e:
        print(str(e))
        return make_response(str(e), 500)



view_cliente = Blueprint("view_cliente", __name__)


@view_cliente.route("/guitarras.html")
def guitarras():
    return render_template("cliente/guitarras.html")


@view_cliente.route("/bajos.html")
def bajos():
    return render_template("cliente/bajos.html")

@view_cliente.route("/productos")
def productos():
    return render_template("cliente/productos.html", productos=productos)


@view_cliente.route("/list_products", methods=["GET"])
def table_data():
    try:
        search = request.args.get("search")
        sort = request.args.get("sort")
        limit = request.args.get("limit")
        offset = request.args.get("offset")

        # obtengo resultados
        total_list = Product.query.filter(Product.description.ilike(f'%{search}%')).count() if search else Product.query.count()
        product_page = Product.query.filter(Product.description.ilike(f'%{search}%')).order_by(Product.price.desc() if sort == 'desc' else Product.price.asc()).offset(int(offset)).limit(int(limit)).all()

        # serializar resultados
        serialized_list = []
        """ for product in product_page:
            serialized_list.append({
                "id": product.id,
                "description": product.description,
                "create_time": str(product.create_time),
                "update_time": str(product.update_time),
                "price": product.price,
                "photo": product.photo,
                "url_nintendo": product.url_nintendo,
            }) """

        serialized_list = [json.loads(json.dumps(product.to_json())) for product in product_page]

        # armar el objeto json response
        response = {"rows": serialized_list, "total": total_list}
        return jsonify(response)

    except Exception as e:
        print(str(e))
        return make_response(str(e), 500)
    #finally:
        # siempre cerrar la sesión, independientemente del resultado
        #db_session.close_all()




@view_cliente.route("/list_p1roducts", methods=["GET"])
def table_data1():
    try:
        my_list = []
        search = request.args.get("search")
        sort = request.args.get("sort")
        limit = request.args.get("limit")
        offset = request.args.get("offset")

        total_list = Product.query.filter(Product.description.ilike(f'%{search}%')).count() if search else Product.query.count()

        product_page = Product.query.filter(Product.description.ilike(f'%{search}%')).order_by(Product.price.desc() if sort == 'desc' else Product.price.asc()).offset(int(offset)).limit(int(limit)).all()


        """ 
        # crear el objeto Query de SQLAlchemy para realizar la consulta
        query = Product.query
        
        # aplicar los filtros
        if search:
            query = query.filter(Product.description.ilike(f'%{search}%'))
            total_list = query.count()
        else:
            total_list = query.count()

        if sort:
            if sort == "desc":
                query = query.order_by(Product.price.desc())
            else:
                query = query.order_by(Product.price.asc())

        if offset:
            query = query.offset(int(offset))

        if limit:
            query = query.limit(int(limit))

        # ejecutar la consulta y obtener los resultados
        product_page = query.all() """

        # serializar resultados
        serialized_list = []
        for product in product_page:
            serialized_product = {
                "id": product.id,
                "description": product.description,
                "create_time": str(product.create_time),
                "update_time": str(product.update_time),
                "price": product.price,
                "photo": product.photo,
                "url_nintendo": product.url_nintendo,
            }

            serialized_list.append(serialized_product)

        # armar el objeto json response
        response = {"rows": serialized_list, "total": total_list}
        return jsonify(response)

    except Exception as e:
        print(str(e))
        return make_response(str(e), 500)
    
