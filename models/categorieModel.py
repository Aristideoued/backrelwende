
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request,jsonify,send_file

from api import db
#db=SQLAlchemy()


class Categorie(db.Model):
    __tablename__='categories'
    id=db.Column(db.Integer,primary_key=True)
    libele=db.Column(db.String(60))
    image=db.Column(db.String(255))


    def __init__(self,libele,image):
        self.libele=libele
        self.image=image
        
        
