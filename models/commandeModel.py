

from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request,jsonify,send_file
from sqlalchemy.dialects.postgresql import JSON
from api import db




class Commande(db.Model):
    __tablename__='commandes'
    id=db.Column(db.Integer,primary_key=True)
    quantite=db.Column(db.Integer)
    date=db.Column(db.String(60))
    dureeLocation=db.Column(db.String(60))
    dateLivraison=db.Column(db.String(60))
    dateLivraisonSouhaite=db.Column(db.String(60))
    dateEvenement=db.Column(db.String(60))
    heure=db.Column(db.String(60))
    heureLivraison=db.Column(db.String(60))
    addresseLivraison=db.Column(db.String(300))
    libele=db.Column(db.String(60))
    statut=db.Column(db.String(60))
    produits=db.Column(JSON)
    client=db.Column(db.Integer)


    def __init__(self,dureeLocation,quantite,date,dateEvenement,dateLivraison,dateLivraisonSouhaite,heure,heureLivraison,addresseLivraison,libele,statut,produits,client):
        self.dureeLocation=dureeLocation
        self.quantite=quantite
        self.date=date
        self.dateEvenement=dateEvenement
        self.dateLivraison=dateLivraison
        self.heure=heure
        self.heureLivraison=heureLivraison
        self.addresseLivraison=addresseLivraison
        self.libele=libele
        self.statut=statut
        self.dateLivraisonSouhaite=dateLivraisonSouhaite
        self.produits=produits
        self.client=client
