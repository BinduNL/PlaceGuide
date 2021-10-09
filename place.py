import json
from flask import Flask, request, jsonify,render_template
from flask_mongoengine import MongoEngine
import requests
import pymongo
from flask_restful import Api,Resource
from pymongo import MongoClient


app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'placeguide',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)

class Place(db.Document):
    name = db.StringField()
    city = db.StringField()
    des=db.StringField()
    def to_json(self):
        return {"name": self.name,
                "city": self.city,
                "des":self.des}

@app.route('/', methods=['GET'])
def query_record():
    name = request.args.get('name')
    p = Place.objects(name=name)
    if not p:	
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(p.to_json())

@app.route('/', methods=['POST'])
def create_record():
    record = json.loads(request.data)
    p = Place(name=record['name'],
                city=record['city'],
                des=record['des'])
    p.save()
    return jsonify(p.to_json())

@app.route('/', methods=['PUT'])
def update_record():
    record = json.loads(request.data)
    p = Place.objects(name=record['name']).first()
    if not p:
        return jsonify({'error': 'data not found'})
    else:
        p.update(city=record['city'])
        p.update(des=record['des'])
        return jsonify(p.to_json())

@app.route('/', methods=['DELETE'])
def delete_record():
    record = json.loads(request.data)
    p = Place.objects(name=record['name']).first()
    if not p:
        return jsonify({'error': 'data not found'})
    else:
        p.delete()
        return jsonify(p.to_json())

@app.route('/home',methods=['GET','POST'])
def home():
    return render_template("home.html")
@app.route('/add',methods=['GET','POST'])
def add():
    if request.method=="GET":
        return render_template("add_places.html")
    else:
        x={
        "name":request.form['name'],
        "city":request.form['city'],
        "des":request.form['des']
        }
        x=json.dumps(x)
        response = requests.post(url="http://127.0.0.1:5000/",data=x)
        return response.text

@app.route('/find',methods=['GET','POST'])
def search():
    if request.method=="GET":
        return render_template("search.html")
    else:
        name=request.form['name']
        response = requests.get(url="http://127.0.0.1:5000/",params={"name":name})
        return response.json()

@app.route('/delete',methods=['GET','POST'])
def delete():
    if request.method=="GET":
        return render_template("delete.html")
    else:
        x={
        "name":request.form['name'],
        
        }
        x=json.dumps(x)
        response = requests.delete(url="http://127.0.0.1:5000/",data=x)
        return response.text

@app.route('/update',methods=['GET','POST'])
def update():
    if request.method=="GET":
        return render_template("update.html")
    else:
        x={
        "name":request.form['name'],
        "city":request.form['city'],
        "des":request.form['des']
        }
        x=json.dumps(x)
        response = requests.put(url="http://127.0.0.1:5000/",data=x)
        return response.text


if __name__ == "__main__":
    place.run(debug=True,host='0.0.0.0',port='5000')
