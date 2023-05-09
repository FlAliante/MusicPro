from flask import Flask, jsonify, request, abort

app = Flask(__name__)

elementos = [
    {
        'id': 1,
        'nombre': 'Elemento 1',
        'descripcion': 'Este es el elemento 1'
    },
    {
        'id': 2,
        'nombre': 'Elemento 2',
        'descripcion': 'Este es el elemento 2'
    }
]

@app.route('/elementos', methods=['GET'])
def obtener_elementos():
    return jsonify({'elementos': elementos})


@app.route('/elementos/<int:id>', methods=['GET'])
def obtener_elemento(id):
    elemento = [elemento for elemento in elementos if elemento['id'] == id]
    if len(elemento) == 0:
        abort(404)
    return jsonify({'elemento': elemento[0]})


@app.route('/elementos', methods=['POST'])
def agregar_elemento():
    if not request.json or not 'nombre' in request.json:
        abort(400)
    elemento = {
        'id': elementos[-1]['id'] + 1,
        'nombre': request.json['nombre'],
        'descripcion': request.json.get('descripcion', "")
    }
    elementos.append(elemento)
    return jsonify({'elemento': elemento}), 201


@app.route('/elementos/<int:id>', methods=['PUT'])
def actualizar_elemento(id):
    elemento = [elemento for elemento in elementos if elemento['id'] == id]
    if len(elemento) == 0:
        abort(404)
    if not request.json:
        abort(400)
    elemento[0]['nombre'] = request.json.get('nombre', elemento[0]['nombre'])
    elemento[0]['descripcion'] = request.json.get('descripcion', elemento[0]['descripcion'])
    return jsonify({'elemento': elemento[0]})

@app.route('/elementos/<int:id>', methods=['DELETE'])
def delete_task(id):
    elemento = [elemento for elemento in elementos if elemento['id'] == id]
    if len(elemento) == 0:
        abort(404)
    elementos.remove(elemento[0])
    return jsonify({'result': True})




