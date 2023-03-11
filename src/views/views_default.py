from . import admin
from sqlalchemy import asc, desc
from src.models import Product
from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify, make_response


@admin.route("/index.html")
def page_index():
    return render_template("default/index.html")


@admin.route("/components-alerts.html")
def components_alerts():
    return render_template("default/components-alerts.html")


@admin.route("/components-accordion.html")
def components_accordion():
    return render_template("default/components-accordion.html")


@admin.route("/pages-register.html")
def pages_register():
    return render_template("default/pages-register.html")


@admin.route("/pages-login.html")
def pages_login():
    return render_template("default/pages-login.html")


@admin.route("/users-profile.html")
def users_profile():
    return render_template("default/users-profile.html")


@admin.route("/pages-faq.html")
def users_faq():
    return render_template("default/pages-faq.html")


@admin.route("/pages-contact.html")
def users_contact():
    return render_template("default/pages-contact.html")


@admin.route("/pages-error-404.html")
def pages_error_404():
    return render_template("default/pages-error-404.html")


@admin.route("/pages-blank.html")
def pages_blank():
    return render_template("default/pages-blank.html")


""" 
@site.route('/portfolio')
def property():
    return render_template('portfolio.html')


@site.route('/properties.html/list', methods=['POST'])
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
 """
