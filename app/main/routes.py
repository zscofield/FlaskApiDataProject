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
neighborhoodsCol = db.neighborhoods

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

except Exception as e:
    print(e)

# CONSTANTS
COMPS = ["gte", "lte"]
def res_json(res):
    return Response(dumps(res), mimetype='application/json')
BLANK_RES = res_json([])
def res_json_pipeline(col, pipeline):
    res = list(col.aggregate(pipeline))
    return res_json(res)
def res_json_find(col, filter):
    res = list(col.find(filter))
    return res_json(res)
def res_json_find_one(col, filter):
    res = col.find_one(filter)
    return res_json(res)

@main.route('/')
def index():
    return '<h1>Hello</h1>'

@main.route('/restaurants/all')
def restaurants_all():
    return res_json_find(restaurantsCol, {})

@main.route('/restaurants/type/<type>')
def restaurants_cat(type):
    return res_json_find(
        restaurantsCol,
        {
            "Category": f"{type}"
        }
    )

@main.route('/restaurants/rating/<comp>/<rating>')
def restaurants_rating(comp, rating):
    if comp in COMPS:
        return res_json_find(restaurantsCol, {"Dining_Rating": {f"${comp}": float(rating)}})
    else:
        return BLANK_RES

@main.route('/restaurants/type/<type>/rating/count/<rcount>')
def restaurants_type_rating_count(type, rcount):
    return res_json_find(
        restaurantsCol,
        {
            "Category": f"{type}",
            "Dining_Review_Count": {"$gte": rcount}
        }
    )

@main.route('/restaurants/type/<type>/rating/<comp>/<rating>')
def restaurants_type_rating(type, comp, rating):
    if comp in COMPS:
        return res_json_find(
            restaurantsCol,
            {
                "Category": f"{type}",
                "Dining_Rating": {f"${comp}": float(rating)}
            }
        )
    else:
        return BLANK_RES

@main.route('/restaurants/price2/<comp>/<price>')
def restaurants_price2(comp, price):
    if comp in COMPS:
        return res_json_find(restaurantsCol, {"Pricing_for_2": {f"${comp}": price}})
    else:
        return BLANK_RES
    
@main.route('/restaurants/near/<lat>,<long>/distance/<distance>')
def restaurants_near(lat, long, distance):
    lat = float(lat)
    long = float(long)
    distance = float(distance)
    filter = {
        "Location": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [long, lat]
                },
                "$maxDistance": distance
            }
        }
    }
    return res_json_find(restaurantsCol, filter)

@main.route('/neighborhoods/all')
def neighborhoods_all():
    return res_json_find(neighborhoodsCol, {})

@main.route('/neighborhoods/location/<lat>,<long>')
def neighborhoods_loc(lat, long):
    lat = float(lat)
    long = float(long)
    return res_json_find_one(
        neighborhoodsCol,
        {
            "geometry": {
                "$geoIntersects":  {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [long, lat]
                    }
                }
            }
        }
    )

@main.route('/restaurants/neighborhood/<n_name>')
def restaurants_neighborhood(n_name):
    n = neighborhoodsCol.find_one({"properties.name": {"$regex": f"{n_name}", "$options": "i"}})
    filter = {
        "Location": {
            "$geoWithin": {
                "$geometry": n["geometry"]
            }
        }
    }
    return res_json_find(restaurantsCol, filter)

@main.route('/restaurants/neighborhood/location/<lat>,<long>')
def restaurants_neighborhood_loc(lat, long):
    lat = float(lat)
    long = float(long)
    n = neighborhoodsCol.find_one(
        {
            "geometry": {
                "$geoIntersects": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [long, lat]
                    }
                }
            }
        }
    )
    filter = {
        "Location": {
            "$geoWithin": {
                "$geometry": n["geometry"]
            }
        }
    }
    return res_json_find(restaurantsCol, filter)