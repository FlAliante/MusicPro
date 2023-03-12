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
