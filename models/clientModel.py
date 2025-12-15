

from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request,jsonify,send_file

from api import db
#db=SQLAlchemy()


class Client(db.Model):
    __tablename__='clients'
    id=db.Column(db.Integer,primary_key=True)
    nom=db.Column(db.String(60))
    prenom=db.Column(db.String(60))
    contact=db.Column(db.String(100))
    email=db.Column(db.String(255))
    password=db.Column(db.String(255))
    code=db.Column(db.String(6))
    aacces=db.Column(db.String(60))
    



    def __init__(self,nom,prenom,contact,email,password):
        self.nom=nom
        self.prenom=prenom
        self.email=email
        self.contact=contact
        self.code=None
        self.aacces=None
        self.password=password
