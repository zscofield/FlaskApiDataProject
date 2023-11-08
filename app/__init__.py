#imports
from flask import Flask
from pymongo import MongoClient
from .extensions import mongo

#routes
from .main.routes import main

def create_app():
    #Creating app instance
    app = Flask(__name__)
    #Connecting to App
    # app.config['MONGO_URI'] = 'mongodb+srv://cit374:yD6Km2LolJm6d5FC@cluster0.mh1tve4.mongodb.net/Pune?retryWrites=true&w=majority'
    #Initializing App
    #mongo.init_app(app)

    #Registering routes
    app.register_blueprint(main)

    return app