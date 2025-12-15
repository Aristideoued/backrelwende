
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request,jsonify,send_file

from api import db
#db=SQLAlchemy()


class ImageModel(db.Model):
    __tablename__='images'
    id=db.Column(db.Integer,primary_key=True)
    #libele=db.Column(db.String(60))
    image=db.Column(db.String(255))
    produit=db.Column(db.Integer)
    numero=db.Column(db.Integer)

    def __init__(self,image,produit,numero):
        #self.libele=libele
        self.image=image
        self.produit=produit
        self.numero=numero