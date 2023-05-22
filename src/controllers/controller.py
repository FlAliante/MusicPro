from flask import Blueprint, jsonify, make_response, redirect, render_template, request, url_for
from config import db_session
from src.models.model import Transaction, Venta, Producto
from src.views.view import app_view
import requests
import json
import random
from datetime import datetime

app_controller = Blueprint("app_controller", __name__)
    
#Creo las credenciales
headers = {
    "Tbk-Api-Key-Id": "597055555532",
    "Tbk-Api-Key-Secret": "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
    "Content-Type": "application/json"
}

# Doc API TRANSBANK https://www.transbankdevelopers.cl/referencia/webpay?l=http#crear-una-transaccion
@app_controller.route("/transaction_create", methods=["POST"])
def  transaction_create():    
    try:
        # Armo el codigo
        fecha_actual = datetime.now()
        date = fecha_actual.strftime("%d%m%y")
        hour = str(fecha_actual.hour).zfill(2)
        minute = str(fecha_actual.minute).zfill(2)
        second = str(fecha_actual.second).zfill(2)
        code = f"{date}-{hour}{minute}{second}-{str(random.randint(100, 999))}"

        # Declaro URL
        url = f"https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions"

        # Creo el JSON
        payload = {
            "buy_order": f"WPB{code}",
            "session_id": f"WPS{code}",
            "amount": float(request.form["amount"]),
            "return_url": f"{request.host_url}crear_commit" # http://127.0.0.1:5000/crear_commit
        }

        #Envio la solicitud
        response = requests.post(url, json=payload, headers=headers)
        
        #Si no es estatus 200 lo saco del metodo
        if response.status_code != 200:
            return make_response(response.json(), response.status_code)
        return response.json()
    except Exception as e:
        return make_response(str(e), 500), print(str(e))
    finally:
        db_session.close_all()

# Doc API TRANSBANK https://www.transbankdevelopers.cl/referencia/webpay?l=http#obtener-estado-de-una-transaccion
@app_controller.route("/transaction_status", methods=["POST"])
def transaction_status():
    try:
        #Obtengo el estado de la transacion segun el token
        url = f"https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{request.form['token']}"
 
        response = requests.get(url, headers=headers)
        #Si no es estatus 200 lo saco del metodo
        if response.status_code != 200:
            return render_template( response.json(), response.status_code)
        
        transaction = Transaction()
        transaction.amount_clp=request.form['amount_clp']
        transaction.amount_usd=request.form['amount_usd']
        transaction.token=request.form['token']
        transaction.url=f"{request.form['url']}?token_ws={request.form['token']}"
        
        data = json.loads(response.content)
        transaction.amount=data['amount']
        transaction.status=data['status']
        transaction.buy_order=data['buy_order'] 
        transaction.session_id=data['session_id'] 
        transaction.accounting_date=data['accounting_date']
        transaction.transaction_date=data['transaction_date']
        transaction.installments_number=data['installments_number']
        db_session.add(transaction)
        db_session.commit()

        # convertir el string JSON a una lista de objetos Python
        lista_objetos = json.loads(request.form['carrito_productos'])

        lista_ventas = []
        # iterar sobre la lista con un for loop
        for objeto in lista_objetos:
            venta = Venta()
            venta.amount_clp = objeto['format']
            venta.id_producto = objeto['id']
            venta.id_transaction = transaction.id
            lista_ventas.append(venta)

        db_session.add_all(lista_ventas)
        db_session.commit()

        #4051 8856 0044 6623
        return redirect(transaction.url)
    except Exception as e:
        contexto = { 'error': True, 'status': 500, 'msj': str(e) }
        return render_template("carrito/pagado.html", **contexto)
    finally:
        db_session.close_all()

# https://www.transbankdevelopers.cl/referencia/webpay?l=http#crear-una-transaccion
@app_controller.route("/crear_commit")
def crear_commit():
    try:
        url = f"https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{request.args.get('token_ws')}"
        
        response = requests.put(url, headers=headers)
        if response.status_code != 200:
            return redirect(url_for('app_view.checkout')) # Corregir y crear una pagina para excepciones

        transaction = db_session.query(Transaction).filter_by(token=request.args.get('token_ws')).first()
        data = json.loads(response.content)
        transaction.vci = data['vci']
        transaction.authorization_code = data['authorization_code']
        transaction.payment_type_code = data['payment_type_code']
        transaction.response_code = data['response_code']
        transaction.card_detail = data['card_detail']
        transaction.amount=data['amount']
        transaction.status=data['status']
        transaction.buy_order=data['buy_order'] 
        transaction.session_id=data['session_id'] 
        transaction.accounting_date=data['accounting_date']
        transaction.transaction_date=data['transaction_date']
        transaction.installments_number=data['installments_number']
        #Con el commit actualizas la tabla
        db_session.commit()
        return redirect(url_for('app_controller.crear_pago', id=transaction.id))
    except Exception as e:
        return make_response(str(e), 500), print(str(e))
    finally:
        db_session.close_all()



#'BUY106-MP468-WP550'
@app_controller.route("/pagado.html/<id>")
def crear_pago(id):
    try:
        # hacer algo si my_string no es un número entero válido
        if id.isdigit():
            transaction = Transaction.query.get(id)
            if transaction:
                #transaction.transaction_date = datetime.strptime(transaction.transaction_date, "%Y-%m-%dT%H:%M:%S.")
                productos = db_session.query(Producto.nombre, Producto.photo, Venta.amount_clp)\
                   .join(Venta, Producto.id == Venta.id_producto)\
                   .filter(Venta.id_transaction == transaction.id).all()

                return render_template("carrito/pagado.html", transaction = transaction, productos = productos)
            else:
                return redirect(request.host_url + "index.html") 
        else:  
            return redirect(request.host_url + "index.html")      
    except Exception as e:
        return make_response(str(e), 500), print(str(e))
    finally:
        db_session.close_all()

# Obsoleto, Ahora se utiliza la
# Trae todos los productos y por tipo de producto 
# http://localhost:5000/get_productos o http://localhost:5000/get_productos?tipo_producto=1
@app_controller.route("/get_productos", methods=["GET"])
def get_productos():
    try:
        tipo_producto = request.args.get("tipo_producto")

        if(tipo_producto):
            url = f"https://music-pro-api.herokuapp.com/api/get_productos?tipo_producto={tipo_producto}"
        else:
            url = "https://music-pro-api.herokuapp.com/api/get_productos"

        response = requests.get(url)
        response.raise_for_status()
        serialized_list = []

        for result in response.json():
            serialized_product = {
                "id": result['id'],
                "nombre": result['nombre'],
                "photo": result['photo'],
                "precio": result['precio'],
                "format_clp": result['format_clp'],
                "marca": result['marca'],
            }
            serialized_list.append(serialized_product)
        return jsonify(serialized_list)
    
    except Exception as e:
        error = { "status": 500, "error": str(e) }
        print(error)
        return make_response(error, 500)