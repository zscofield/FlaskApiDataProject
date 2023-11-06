from flask import Flask, Blueprint, Response, render_template
from ..extensions import mongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import ssl
from bson.json_util import dumps, loads
#import certifi

main = Blueprint('main', __name__)

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

comps = ["gte", "lte"]

@main.route('/')
def index():
    return '<h1>Hello</h1>'

@main.route('/restaurants/all')
def restaurants_all():
    pipeline = []
    res = list(restaurantsCol.aggregate(pipeline))

    return Response(dumps(res), mimetype='application/json')

@main.route('/restaurants/type/<type>')
def restaurants_cat(type):
    pipeline = [
        {"$match": {"Category": f"{type}"}}
    ]
    res = list(restaurantsCol.aggregate(pipeline))

    return Response(dumps(res), mimetype='application/json')

@main.route('/restaurants/rating/<comp>/<rating>')
def restaurants_rating(comp, rating):
    if comp in comps:
        pipeline = [
            {"$match": {"Dining_Rating": {f"${comp}": float(rating)}}}
        ]
        res = list(restaurantsCol.aggregate(pipeline))
    else:
        res = []

    return Response(dumps(res), mimetype='application/json')

@main.route('/restaurants/type/<type>/rating/<comp>/<rating>')
def restaurants_type_rating(type, comp, rating):
    if comp in comps:
        pipeline = [
            {
                "$match": {
                    "Category": f"{type}",
                    "Dining_Rating": {f"${comp}": float(rating)}
                }
            }
        ]
        res = list(restaurantsCol.aggregate(pipeline))
    else:
        res = []

    return Response(dumps(res), mimetype='application/json')