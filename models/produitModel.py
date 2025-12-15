


from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request,jsonify,send_file
from sqlalchemy.dialects.postgresql import JSON
from api import db
#db=SQLAlchemy()

class Produit(db.Model):
    __tablename__='produits'
    id=db.Column(db.Integer,primary_key=True)
    reference=db.Column(db.String(60))
    libele=db.Column(db.String(60))
    typeEmballage=db.Column(db.String(60))
    stock=db.Column(db.Integer)
    categorie=db.Column(db.Integer)
    prix=db.Column(db.Integer)
    description=db.Column(db.Text)
    prixReduit=db.Column(db.Integer)
    couleur=db.Column(db.String(60))
    index=db.Column(db.Integer)
    extend=db.Column(JSON)

    #image=db.Column(db.String(60))


    def __init__(self,reference,libele,stock,categorie,prix,prixReduit,description):
        self.reference=reference
        self.libele=libele
        self.stock=stock
        self.categorie=categorie
        self.prix=prix
        self.description=description,
        #self.image=image
        self.prixReduit=prixReduit
        self.typeEmballage=None
        self.couleur=None
        self.index=0

    

    def info(self):
            """Build a dictionary structure of a artist model.

            Returns:
            The dictionary content of the artist model.
            """
            data = {
           
            'id': self.id,
            'libele': self.libele,
            'reference': self.reference,
            'stock': self.stock,
            'categorie': self.categorie,
            'prix': self.prix,
            'prixReduit': self.prixReduit,
            'typeEmballage': self.typeEmballage,
            'description': self.description,
           
            'couleur': self.couleur,
            'index': self.index

            }

            return data

    def extended(self):
        """Add the extend field to the built dictionary content.

        Returns:
          The augmented dictionary.
        """
        data = self.info()
        data['extend'] = self.extend
        return data

