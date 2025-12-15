

from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request,jsonify,send_file
from sqlalchemy.dialects.postgresql import JSON
from api import db




class Panier(db.Model):
    __tablename__='paniers'
    id=db.Column(db.Integer,primary_key=True)
    taille=db.Column(db.Integer)
    total=db.Column(db.Integer)
    totalReduit=db.Column(db.Integer)
    statut=db.Column(db.String(60))
    client=db.Column(db.Integer)
    produits=db.Column(JSON)
    


    def __init__(self,taille,total,statut,client,produits,totalReduit):
        self.taille=taille
        self.total=total
        self.total=totalReduit
        self.statut=statut
        self.client=client
        self.produits=produits
