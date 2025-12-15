import os
import sys
from api import app as application
from api import db
from api.endpoints import *

from models.adminModel import Admin
from models.categorieModel import Categorie
from models.clientModel import Client
from models.commandeModel import Commande
from models.entreeModel import Entree
from models.imageModel import ImageModel
from models.panierModel import Panier
from models.produitModel import Produit
from models.distributionImageModel import DistributionImageModel
from models.distributionPanierModel import DistributionPanier
from models.locationImageModel import LocationImageModel
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler

sys.path.insert(0, os.path.dirname(__file__))


def applications(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    message = 'It works!\n'
    version = 'Python v' + sys.version.split()[0] + '\n'
    response = '\n'.join([message, version])
    return [response.encode()]
    
application.logger.setLevel(logging.INFO)
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
application.logger.addHandler(handler)


if __name__ == "__main__":
    
    application.run(host='0.0.0.0')
