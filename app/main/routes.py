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

# CONSTANTS
COMPS = ["gte", "lte"]
BLANK_RES = Response(dumps([]), mimetype='application/json')
def res_json(pipeline):
    res = list(restaurantsCol.aggregate(pipeline))
    return Response(dumps(res), mimetype='application/json')

@main.route('/')
def index():
    return '<h1>Hello</h1>'

@main.route('/restaurants/all')
def restaurants_all():
    pipeline = []
    return res_json(pipeline)

@main.route('/restaurants/type/<type>')
def restaurants_cat(type):
    pipeline = [
        {"$match": {"Category": f"{type}"}}
    ]
    return res_json(pipeline)

@main.route('/restaurants/rating/<comp>/<rating>')
def restaurants_rating(comp, rating):
    if comp in COMPS:
        pipeline = [
            {"$match": {"Dining_Rating": {f"${comp}": float(rating)}}}
        ]
        return res_json(pipeline)
    else:
        return BLANK_RES

@main.route('/restaurants/type/<type>/rating/count/<rcount>')
def restaurants_type_rating_count(type, rcount):
    pipeline = [
        {
            "$match": {
                "Category": f"{type}",
                "Dining_Review_Count": {"$gte": rcount}
            }
        }
    ]
    return res_json(pipeline)

@main.route('/restaurants/type/<type>/rating/<comp>/<rating>')
def restaurants_type_rating(type, comp, rating):
    if comp in COMPS:
        pipeline = [
            {
                "$match": {
                    "Category": f"{type}",
                    "Dining_Rating": {f"${comp}": float(rating)}
                }
            }
        ]
        return res_json(pipeline)
    else:
        return BLANK_RES

@main.route('/restaurants/price2/<comp>/<price>')
def restaurants_price2(comp, price):
    if comp in COMPS:
        pipeline = [{"$match": {"Pricing_for_2": {f"${comp}": price}}}]
        return res_json(pipeline)
    else:
        return BLANK_RES