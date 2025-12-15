
import flask as fk
from flask import Flask
from flask_httpauth import HTTPBasicAuth
import json
import logging
from flask_migrate import Migrate
from flask_cors import CORS
import hashlib
from flask_sqlalchemy import SQLAlchemy
from functools import update_wrapper
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "https://admin.relwende.com"}},supports_credentials=True)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://c2392788c_Aristide:2885351Aristide12@localhost/c2392788c_relwende'
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'postgresql+psycopg2://postgres:2885351@localhost:5432/relwende'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db=SQLAlchemy(app)

migrate=Migrate(app,db)

from models.adminModel import Admin




auth = HTTPBasicAuth()

#db=SQLAlchemy()

"""logger = logging.getLogger("relwendeapi")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('/home/c2392788c/public_html/relwendeapi/app.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)

@app.after_request
def after_request(response):
    # Toujours loguer, même si c'est une réponse CORS automatique
    logger.info(">>> Headers envoyés: %s", response.headers)
    return response"""




@auth.verify_password
def authenticate(username, password):
    hashed_password = hashlib.sha256((password).encode("ascii")).hexdigest()
    admin=db.session.query(Admin).filter(Admin.password==hashed_password).filter(Admin.username==username).first()
    #admin2=db.session.query(Admin).filter(Admin.username==username).first()
    if admin :
      return True
    else:
      return False
    return False
    

