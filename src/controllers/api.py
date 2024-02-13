import base64
from flask import Blueprint, jsonify, make_response, request
from sqlalchemy.sql.expression import func
from sqlalchemy import text

from config import db_session
from src.models.model import Producto, Venta, Transaction

import requests
import locale
import os
from sqlalchemy import text

api_producto = Blueprint("api_producto", __name__)

class ProductoController():
    # Api Producto https://music-pro-api.herokuapp.com/api/productos?tipo_producto=1 -> te devuelve guitarras
    @api_producto.route('/api/get_productos', methods=['GET'])
    def get_productos():
        try:
            #Obtengo variables cargadas en la URL
            tipo_producto = request.args.get("tipo_producto")
            if tipo_producto:
                productos = Producto.query.filter(Producto.tipo_producto == tipo_producto)
            else:
                #Obtengo 8 datos aleatorios
                productos = Producto.query.order_by(func.random()).limit(8).all()

            #Creo una lista para guardar los productos
            serialized_list = []
            for producto in productos:
                serialized_producto = {
                    "Serie del producto": "EC-" + str(Producto.random_integer(100, 999)),
                    "codigo": f"{Producto.random_letters(3)}-{Producto.random_integer(1000, 9999)}",
                    "marca": producto.marca.strip(),
                    "id": producto.id,
                    "id_tipo_producto": producto.tipo_producto,
                    "nombre": producto.nombre,
                    "photo": producto.photo,
                    "precio": producto.precio,
                    "format_clp": ProductoController.format_price_clp(producto.precio),         
                    "fecha_actualizacion": producto.fecha_actualizacion,
                    "fecha_creacion": producto.fecha_creacion,
                    "serie": [
                        {
                            "fecha": producto.fecha_creacion,
                            "valor": producto.precio
                        }
                    ],
                }
                serialized_list.append(serialized_producto)
            return jsonify(serialized_list)
        except Exception as e:
            print(str(e))
            return make_response({'status': 500, 'error': str(e)}, 500)
        finally:
            db_session.close_all()
    # Converidor de Moneda https://music-pro-api.herokuapp.com/api/exchange_rate?amount_clp=1000
    @api_producto.route('/api/exchange_rate', methods=['GET'])
    def exchange_rate():
        try:
            amount_clp  = request.args.get("amount_clp")
            if amount_clp :
                url = f'https://v6.exchangerate-api.com/v6/534569873736672ef33d04ea/pair/CLP/USD/{amount_clp}'
            else:
                msj = {
                    'status': 500, 
                    'error': 'Debes ingresar el monto (amount_clp) para transformarlo a dolar. Example https://music-pro-api.herokuapp.com/amount_clp=1000'
                }
                return make_response(msj,  500)
            response = requests.get(url)
            data = response.json()

            # Establece el idioma y la ubicación para el formato
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

            # Formatea el precio con separadores de miles y símbolo de dólar USD
            serialized = {
                "result": data['conversion_result'],
                "format": locale.currency(data['conversion_result'], grouping=True, symbol='USD'),
            }
            return jsonify(serialized)
        except Exception as e:
            print(str(e))
            return make_response({'status': 500, 'error': str(e)}, 500)

    def format_price_clp(price):
        # Obtiene el valor entero y decimal del precio
        price_str = str(price)
        if '.' not in price_str:
            int_part = price_str
            dec_part = ''
        else:
            int_part, dec_part = price_str.split('.')

        # Divide la parte entera en grupos de tres dígitos y los une con puntos
        int_part = '.'.join(reversed([int_part[max(i-3, 0):i] for i in range(len(int_part), 0, -3)]))

        # Devuelve la cadena formateada en pesos chilenos (CLP)
        return f"${int_part}" + (f",{dec_part}" if dec_part else "")

class VentaController():
    @api_producto.route('/api/venta/status/<status>', methods=['GET'])
    def get_venta_for(status):
        try:
            sql_statement = text(f"CALL ObtenerVentasConDetallePorEstadoTransaccion('{status}')")
            result = db_session.execute(sql_statement).all()
            
            # Lista para almacenar diccionarios
            list_result = []

            for item in result:
                # Crear un diccionario para cada fila
                row_dict = {}
                
                for field in item._fields:
                    row_dict[field] = item._mapping[field]
                
                list_result.append(row_dict)

            return jsonify(list_result)

        except Exception as e:
            print(str(e))
            return make_response({'status': 500, 'error': str(e)}, 500)
        finally:
            db_session.close_all()
    
    @api_producto.route('/api/venta', methods=['GET'])
    def get_venta():
        try:
            sql_statement = text("CALL ObtenerVentasConDetalle()")
            result = db_session.execute(sql_statement).all()
            
            # Lista para almacenar diccionarios
            list_result = []

            for item in result:
                # Crear un diccionario para cada fila
                row_dict = {}
                
                for field in item._fields:
                    row_dict[field] = item._mapping[field]
                
                list_result.append(row_dict)

            return jsonify(list_result)

        except Exception as e:
            print(str(e))
            return make_response({'status': 500, 'error': str(e)}, 500)
        finally:
            db_session.close_all()

class TransactionController():
    @api_producto.route('/api/transaction', methods=['GET'])
    def get():
        try:
            # Obtengo variables cargadas en la URL
            transactions = Transaction.query.filter(Transaction.status == "AUTHORIZED").all()

            # Convertir las transacciones a una lista de diccionarios
            transaction_list = [transaction.to_dict() for transaction in transactions]

            return jsonify(transaction_list)
        except Exception as e:
            print(str(e))
            return make_response({'status': 500, 'error': str(e)}, 500)
        finally:
            db_session.close_all()

    @api_producto.route('/api/test_adjunto', methods=['POST'])
    def post():
        try:
            file_path = "C:/Users/Usuario/Downloads/"

            # Verifica si se enviaron archivos
            if 'file' not in request.files:
                return jsonify({'message': 'No se enviaron archivos'}), 400

            # Obtiene los archivos enviados
            files = request.files.getlist('file')

            # Decodificar y guardar los archivos en la ruta especificada
            for file in files:
                # Decodificar el contenido base64
                decoded_content = base64.b64decode(file.read())
                filename = file.filename

                # Guardar el archivo decodificado
                with open(os.path.join(file_path, filename), 'wb') as f:
                    f.write(decoded_content)

            return jsonify({'message': 'Documentos enviados con éxito'})
        except Exception as e:
            print(str(e))
            return make_response({'status': 500, 'error': str(e)}, 500)
        finally:
            db_session.close_all()

    @api_producto.route('/api/test_adjunto_json', methods=['POST'])
    def post_json():
        try:
            # Ruta donde se guardarán los archivos
            file_path = "C:/Users/Usuario/Downloads/"

            # Verifica si se recibió un JSON en la solicitud
            if request.json is None:
                return jsonify({'message': 'No se recibió un JSON'}), 400


            # Obtiene la lista de archivos del JSON
            files = request.json

            # Guarda los archivos en la ruta especificada
            for file_data in files:
                filename = file_data['filename']
                file_content = file_data['fileContent']
                # Decodifica el contenido base64
                file_content_decoded = base64.b64decode(file_content)
                # Escribe el contenido en el archivo
                with open(os.path.join(file_path, filename), 'wb') as f:
                    f.write(file_content_decoded)

            return jsonify({'message': 'Documentos enviados con éxito'})
        except Exception as e:
            print(str(e))
            return make_response({'status': 500, 'error': str(e)}, 500)
        
    @api_producto.route('/api/test_adjunto_descarga', methods=['POST'])
    def test_adjunto_descarga():  
        base_url = "https://test.salesforce.com"
        endpoint = "/services/oauth2/token"
        grant_type = "password"
        client_id = "3MVG9j6uMOMC1DNgb228MoMe2FVkscJQ0bv2IHsNpF80ouPWMCxVyPEKrBs.0w9XSOkoKqXt2sV7wJGNP_YvU"
        client_secret = "E6CC5003E4172DF13D4F83E07C1C625EBAF3724E42F6EAF6F8070EB22A7EACA8"
        username = "consultor@vasslatam-security.com.sbxvass3"
        password = "Vasslatam2022*XOGh34klsHmtZPYIt17neiKYa"

        url = f"{base_url}{endpoint}?grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}&username={username}&password={password}"

        payload = {}
        headers = {}

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

        data = response.json()
        access_token = data['access_token']
        instance_url = data['instance_url']

        url = f"{instance_url}/services/data/v60.0/query/?q=SELECT+id,VersionData,FileType,Title,FileExtension,PathOnClient+FROM+ContentVersion"

        payload = {}
        headers = {
          'Authorization': f'Bearer {access_token}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 200:
            json_data = response.json()
        else:
            return jsonify({'message': f"Error al obtener los datos: {response.status_code}"})
        
        for record in json_data['records']:
            response = requests.request("GET", f"{instance_url}{record['VersionData']}", headers=headers, data=payload)
            if response.status_code == 200:
                #full_path = f"C:/Users/Usuario/Downloads/"
                #record_folder = os.path.join(full_path, record['Id'])
                #os.makedirs(record_folder, exist_ok=True)

                with open(f"C:/Users/Usuario/Downloads/{record['Id']} - {record['PathOnClient']}" , "wb") as f:
                    f.write(response.content)
            else:
                return jsonify({'message': 'Documentos enviados sin éxito'})
        
        return jsonify({'message': 'Documentos enviados con éxito'})





        
 