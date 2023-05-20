import engineio
from flask import Blueprint, jsonify, make_response, redirect, render_template, request
from sqlalchemy import engine_from_config
from config import db_session, engine
from src.models.model import Transaction
import requests
import json
import random


app_controller = Blueprint("view_cliente", __name__)

headers = {
    "Tbk-Api-Key-Id": "597055555532",
    "Tbk-Api-Key-Secret": "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
    "Content-Type": "application/json"
}

# Doc API TRANSBANK https://www.transbankdevelopers.cl/referencia/webpay?l=http#confirmar-una-transaccion
@app_controller.route("/pagar_transkbank", methods=["POST"])
def pagar_transkbank():
    try:
        amount_clp = request.form['amount_clp']
        amount_usd = request.form["amount_usd"]
        buy_order = f"BUY{str(random.randint(100, 999))}-MP{str(random.randint(100, 999))}-WP{str(random.randint(100, 999))}"
        session_id = buy_order
        url_actual = request.host_url
                    
        # Creo el pago
        url = f"https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions"
        payload = {
            "buy_order": buy_order,
            "session_id": session_id,
            "amount": amount_clp,
            "return_url": url_actual + "pagado.html"
            #"return_url": url_actual + "pagado/" + buy_order
        }

        #Recibo en formato json
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            token = response.json()['token']
            new_url = f"{response.json()['url']}?token_ws={token}" 
            url = f"https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{token}"

            response = requests.get(url, headers=headers)

            result = response.json()
            transaction = Transaction(
                vci = '', 
                card_number='', 
                authorization_code= '', 
                payment_type_code='', 
                response_code = '',
                amount=result['amount'], 
                status=result['status'], 
                buy_order=result['buy_order'], 
                session_id=result['session_id'], 
                accounting_date=result['accounting_date'], 
                transaction_date=result['transaction_date'], 
                installments_number=result['installments_number'], 
                token=token, 
                url=new_url
            )

            db_session.add(transaction)
            db_session.commit()

            return jsonify(buy_order)
        else: 
            return make_response(jsonify(response.json()), response.status_code)
    except Exception as e:
        print(str(e))
        return make_response(str(e), 500)
    finally:
        db_session.close_all()
   

@app_controller.route("/redireccionarWebPay", methods=["POST"])
def redireccionarWebPay():
    buy_order = request.form["buy_order"]    
    transaction = Transaction.query.filter(Transaction.buy_order == buy_order)
    url = ''
    for item in transaction:
        url = item.url
    return redirect(url)



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
    

 