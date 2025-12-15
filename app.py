import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
import hashlib
from api.endpoints import *
from api import app,db,auth,authenticate

from models.adminModel import Admin
from models.categorieModel import Categorie
from models.clientModel import Client
from models.commandeModel import Commande
from models.entreeModel import Entree
from models.imageModel import ImageModel
from models.panierModel import Panier
from models.produitModel import Produit
from models.distributionImageModel import DistributionImageModel
from models.locationImageModel import LocationImageModel

app.logger.setLevel(logging.INFO)
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)





@app.route('/')
def home():
    return "Hello, Flask!"


@app.route('/initdb',methods=['GET'])
def create_table():
    db.create_all()
  
    return "Tables created"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
