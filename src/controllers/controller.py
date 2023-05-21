from flask import Blueprint, jsonify, make_response, redirect, render_template, request
from sqlalchemy import engine_from_config
from config import db_session, engine
from src.models.model import Transaction
import requests
import json
import random
import datetime

app_controller = Blueprint("view_cliente", __name__)

# Doc API TRANSBANK https://www.transbankdevelopers.cl/referencia/webpay?l=http#confirmar-una-transaccion
@app_controller.route("/pagar_transkbank", methods=["POST"])
def pagar_transkbank():    
    try:
        transaction = Transaction()
        db_session.add(transaction)
        db_session.commit()

        fecha_actual = datetime.date.today()
        fecha_formateada = fecha_actual.strftime("%d%m%Y")

        # Declaro URL
        url = f"https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions"

        # Creo el JSON
        payload = {
            "buy_order": f"BUY{fecha_formateada}-MP{str(random.randint(100, 999))}-WP{str(random.randint(100, 999))}",
            "session_id": f"SES{fecha_formateada}-MP{str(random.randint(100, 999))}-WP{str(random.randint(100, 999))}",
            "amount": request.form["amount"],
            "return_url": f"{request.host_url}pagado/{transaction.id}" # http://127.0.0.1:5000/pagado/{buy_order}
        }

        #Creo las credenciales
        headers = {
            "Tbk-Api-Key-Id": "597055555532",
            "Tbk-Api-Key-Secret": "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
            "Content-Type": "application/json"
        }

        #Envio la solicitud
        response = requests.post(url, json=payload, headers=headers)
        
        #Si no es estatus 200 lo saco del metodo
        if response.status_code != 200:
            return make_response(response.json(), response.status_code)
            
        #Rescato el resultado en formato json 
        data = response.json()
        token = data['token']
        url = data['url']
        url_create = f"{url}?token_ws={token}"

        #Obtengo el estado de la transacion segun el token
        url = f"https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{token}"
        response = requests.get(url, headers=headers)

        #Si no es estatus 200 lo saco del metodo
        if response.status_code != 200:
            return make_response(response.json(), response.status_code)

        #Obtengo el resultado segun formato
        data = json.loads(response.content)

        transaction.amount=data['amount']
        transaction.status=data['status']
        transaction.buy_order=data['buy_order'] 
        transaction.session_id=data['session_ida'] 
        transaction.accounting_date=data['accounting_date']
        transaction.transaction_date=data['transaction_date']
        transaction.installments_number=data['installments_number']

        transaction.amount_clp=request.form['amount_clp']
        transaction.amount_usd=request.form['amount_usd']

        transaction.token=token
        transaction.url=url_create

        db_session.commit()
        #4051 8856 0044 6623
        return jsonify(transaction.id)
    
    except Exception as e:
        return make_response(str(e), 500),  print(str(e))
    finally:
        db_session.close_all()


@app_controller.route("/redireccionarWebPay", methods=["POST"])
def redireccionarWebPay():
    id = request.form["buy_order"]
    # Busca la transsaccion por id    
    transaction = Transaction.query.get(id)
    return redirect(transaction.url)


#'BUY106-MP468-WP550'
@app_controller.route("/pagado/<id>")
def pagadoasd(id):
    try:
        transaction = Transaction.query.get(id)

        url = f"https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{transaction.token}"

        headers = {
            "Tbk-Api-Key-Id": "597055555532",
            "Tbk-Api-Key-Secret": "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
            "Content-Type": "application/json"
        }
        
        response = requests.put(url, headers=headers)
        if response.status_code != 200:
            return make_response(response.json(), response.status_code)

        data = json.loads(response.content)

        transaction.vci = data['vci']
        transaction.authorization_code = data['authorization_code']
        transaction.payment_type_code = data['payment_type_code']
        transaction.response_code = data['response_code']
        transaction.card_detail = data['card_detail']

        #Con el commit actualizas la tabla
        db_session.commit()

        return redirect(request.host_url + "pagado.html") # render_template("carrito/pagado.html")
    except Exception as e:
        print(str(e))
        return make_response(str(e), 500)
    finally:
        db_session.close_all()






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
    
