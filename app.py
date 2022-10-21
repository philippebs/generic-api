from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from flask import request
import os
import requests
import util
from model import Server
import platform
import json

#Inicializa nossa aplicacao Flask
app =  Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


#Cria a rota para o caminho
@app.route("/")
@cross_origin()
def index():
	return render_template('index.html')


@app.route("/<file_name>", methods=['GET', 'POST', 'PUT', 'DELETE'])
@cross_origin()
def index_json(file_name):
    json_file = util.ler_json_file(file_name)

    if request.method == 'GET':
        return json_file

    json_data = json.loads(json_file)
    if request.method == 'POST':
        if request.data:

            rcv_data = json.loads(request.data.decode(encoding='utf-8'))
            json_data.append(rcv_data)
            set_id(json_data=json_data)
            sort_json(json_data=json_data)

            util.salvar_json(name=file_name, list_dados=json_data)
            return '200'
        else:
            return '404'

    rcv_data = None
    if request.data:
        rcv_data = json.loads(request.data.decode(encoding='utf-8'))

    if not rcv_data['id']:
        return '404'
        
    item_one = get_one(id=int(rcv_data['id']), json_data=json_data)

    if not item_one:
        return '404'
    
    json_data = [item for item in json_data if not (item['id'] == item_one['id'])]
    if request.method == 'PUT':
        json_data.append(rcv_data)
        json_data = sort_json(json_data=json_data)

    util.salvar_json(name=file_name, list_dados=json_data)
    return '200'


def sort_json(json_data):
    return sorted(json_data, key=lambda d: d['id']) 


@app.route("/<file_name>/<id>", methods=['GET'])
@cross_origin()
def find_item(file_name, id):
    json_file = util.ler_json_file(file_name)

    json_data = json.loads(json_file)
    data = get_one(id=int(id), json_data=json_data)

    if request.method == 'GET':
        return data if data else {} 


def get_max_id(json_data):
    max_id = 0
    for item_json in json_data:
        for key in item_json.keys():
            if str(key).lower() == 'id':
                id = int(item_json[key])
                if id > max_id:
                    max_id = id

    return max_id


def set_id(json_data):
    id = get_max_id(json_data=json_data)
    for item_json in json_data:
        contem_id = False
        for key in item_json.keys():
            if str(key).lower() == 'id':
                contem_id = True
                break
        if not contem_id:
            id += 1
            item_json['id'] = id


def get_one(id, json_data):
    for item_json in json_data:
        if item_json['id'] == id:
            return item_json
    return None


@app.route('/create/<file>', methods=['POST'])
@cross_origin()
def crete(file):
    if request.method == 'POST':
        if request.data:
            json_data = json.loads(request.data.decode(encoding='utf-8'))
            set_id(json_data)

            util.salvar_json(name=file, list_dados=json_data)
            if util.exists_json(file):
                return '200'
    return '404'



#Executa nossa aplicacao
if __name__ == "__main__":
    # so = platform.system()
    # if so != "Windows":
    #     os.chdir('/home')
    # port = int(os.environ.get("PORT", 5000))
    app.run(debug=True)