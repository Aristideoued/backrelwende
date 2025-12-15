

from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request,jsonify,send_file

from api import db


class Admin(db.Model):
    __tablename__='admins'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(60))
    nom=db.Column(db.String(60))
    prenom=db.Column(db.String(60))
    password=db.Column(db.String(255))



    def __init__(self,nom,prenom,username,password):
        self.nom=nom
        self.prenom=prenom
        self.username=username
        self.password=password
