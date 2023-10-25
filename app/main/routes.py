from flask import Flask, Blueprint, render_template, jsonify
from ..extensions import mongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import ssl
#import certifi

main = Blueprint('main', __name__)
name = Blueprint('name', __name__)
restaurantsAll = Blueprint('restaurants', __name__)
restaurantsAllType = Blueprint('restaurants_cat', __name__)


#ca = certifi.where()
uri = "mongodb+srv://zach:qgUwp5xFOh4hPiSe@cluster0.mh1tve4.mongodb.net/?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client.Pune # db reference
restaurantsCol = db.restaurants

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

except Exception as e:
    print(e)

@main.route('/')
def index():
    return '<h1>Hello</h1>'

@name.route('/<name>')
def indexName(name):
    return '<h1>Hello {}</h1>'.format(name)

@restaurantsAll.route('/restaurants/all')
def all_restaurants():
    # pipeline = [{"$project": {"Restaurant_Name": "$Restaurant_Name"}}]
    pipeline = []
    res = list(restaurantsCol.aggregate(pipeline))
    res_str = ''

    # returns all restaurant names, and Ids in an array
    # for i in res:
    #     res_str += f'{i}<br/>'
    # return res_str

    # returns all restaurant namea in a html file
    return render_template('index.html', r=res)

@restaurantsAllType.route('/restaurants/all/type/<type>')
def all_restaurants_cat(type):
    pipeline = [
        {"$match": {"Category": f"{type}"}}
        # , {"$project": {"Restaurant_Name": "$Restaurant_Name"}}
    ]
    res = list(restaurantsCol.aggregate(pipeline))

    # returns all restaurant namea in a html file
    return render_template('index.html', r=res)

