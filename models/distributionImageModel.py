
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,request,jsonify,send_file

from api import db

class DistributionImageModel(db.Model):
    __tablename__='distributions_images'
    id=db.Column(db.Integer,primary_key=True)
    #libele=db.Column(db.String(60))
    image=db.Column(db.String(255))
   

    def __init__(self,image):
        #self.libele=libele
        self.image=image