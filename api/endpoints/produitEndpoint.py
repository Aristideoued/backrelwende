from flask import Blueprint, jsonify, request, make_response, send_file
from PIL import Image
import os
from models.produitModel import Produit
from models.categorieModel import Categorie
from models.imageModel import ImageModel
from api import app,db,auth,authenticate
from wsgi import DistributionImageModel, LocationImageModel

from flask_cors import cross_origin

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MYDIR = os.path.dirname(__file__)

@app.route('/addProduit' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def addProduit():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':

            data = request.get_json()

            libele=data['libele']
            reference=data['reference']
            stock=int(data['stock'])
            categorie=int(data['categorie'])
            prix=int(data['prix'])
            #prixReduit=int(data['prixReduit'])
            prixReduit=0
            description=data['description']
            
            if "prixReduit" in data:
                prixReduit=int(data['prixReduit'])
                
            else:
                prixReduit=prix
               
           
            produit=Produit(reference,libele,stock,categorie,prix,prixReduit,description)
            produit.index=0
            db.session.add(produit)
            db.session.commit()

           
                
                
            if "typeEmballage" in data:
                produit.typeEmballage=data['typeEmballage']
                db.session.add(produit)
                db.session.commit()

            if "couleur" in data:
                produit.couleur=data['couleur']
                db.session.add(produit)
                db.session.commit()

            retour={"code":200,"title":"Ajout d'un produit","contenu":"Produit ajouté avec succes"}
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)

@app.route('/produitById' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getProduitById():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            produits=[]
            data = request.get_json()

            id=int(data['id'])

            produit=db.session.query(Produit).filter(Produit.id==id).first()

           
            categorie=db.session.query(Categorie).filter(Categorie.id==produit.categorie).first()   
            
            image=db.session.query(ImageModel).filter(ImageModel.produit==id)
            images=[]
                
            for im  in image:
                images.append({"id":im.id,"numero":im.numero,"url":"https://backend.relwende.com/produitImagesMultiple/"+str(id)+"/"+str(im.numero)
                })
            produits.append({"id":produit.id,"reference":produit.reference,"libele":produit.libele,"description":produit.description,"stock":produit.stock,"idCategorie":produit.categorie,"libeleCategorie":categorie.libele,"couleur":produit.couleur,"prix":produit.prix,"prixReduit":produit.prixReduit,"typeEmballage":produit.typeEmballage,"images":images})


            retour={"code":200,"title":"Produit "+str(id),"contenu":produits}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)

@app.route('/produitByCategorie' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getProduitByCat():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            produits=[]
            data = request.get_json()

            id=int(data['id'])

            produit=db.session.query(Produit).filter(Produit.categorie==id)

            for f in produit:
                #print(u.nom)
                categorie=db.session.query(Categorie).filter(Categorie.id==f.categorie).first()
                
                image=db.session.query(ImageModel).filter(ImageModel.produit==f.id)
                images=[]
                
                for im  in image:
                    images.append({"id":im.id,"numero":im.numero,"url":"https://backend.relwende.com/produitImagesMultiple/"+str(f.id)+"/"+str(im.numero)
                    })
                    
                produits.append({"id":f.id,"reference":f.reference,"libele":f.libele,"description":f.description,"stock":f.stock,"idCategorie":f.categorie,"libeleCategorie":categorie.libele,"couleur":f.couleur,"prix":f.prix,"prixReduit":f.prixReduit,"typeEmballage":f.typeEmballage,"images":images})


            retour={"code":200,"title":"Produit de la categorie "+str(id),"contenu":produits}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)



@app.route('/distribution' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getProduitByCatDistri():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='GET':
            produits=[]
            categorie=db.session.query(Categorie).filter(Categorie.libele=="BOISSON").first()            


            produit=db.session.query(Produit).filter(Produit.categorie==categorie.id)

            for f in produit:
                #print(u.nom)
                categorie=db.session.query(Categorie).filter(Categorie.id==f.categorie).first()  
                
                image=db.session.query(ImageModel).filter(ImageModel.produit==f.id)
                images=[]
                
                for im  in image:
                    images.append({"id":im.id,"numero":im.numero,"url":"https://backend.relwende.com/produitImagesMultiple/"+str(f.id)+"/"+str(im.numero)
                    })
                produits.append({"id":f.id,"reference":f.reference,"libele":f.libele,"description":f.description,"stock":f.stock,"idCategorie":f.categorie,"libeleCategorie":categorie.libele,"couleur":f.couleur,"prix":f.prix,"prixReduit":f.prixReduit,"typeEmballage":f.typeEmballage,"images":images})


            retour={"code":200,"title":"Produit de la categorie "+str(id),"contenu":produits}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)




@app.route('/produits' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getProduit():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='GET':
            produits=[]
           
            produit = Produit.query.all()
            #user=db.session.query(User).all()

            for f in produit:
                #print(f.description)
                categorie=db.session.query(Categorie).filter(Categorie.id==f.categorie).first()
                
                image=db.session.query(ImageModel).filter(ImageModel.produit==f.id)
                images=[]
                
                for im  in image:
                    images.append({"id":im.id,"numero":im.numero,"url":"https://backend.relwende.com/produitImagesMultiple/"+str(f.id)+"/"+str(im.numero)
                    })
                if   categorie.libele !="BOISSON":
                    
                     produits.append({"id":f.id,"reference":f.reference,"libele":f.libele,"description":f.description,"stock":f.stock,"idCategorie":f.categorie,"libeleCategorie":categorie.libele,"couleur":f.couleur,"prix":f.prix,"prixReduit":f.prixReduit,"typeEmballage":f.typeEmballage,"images":images})


            retour={"code":200,"title":"Liste des produits","contenu":produits}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode GET"}
      return make_response(jsonify(retour),403)


@app.route('/all/produits' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getProduitAll():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='GET':
            produits=[]
           
            produit = Produit.query.all()
            #user=db.session.query(User).all()

            for f in produit:
                #print(f.description)
                categorie=db.session.query(Categorie).filter(Categorie.id==f.categorie).first()
                
                image=db.session.query(ImageModel).filter(ImageModel.produit==f.id)
                images=[]
                
                for im  in image:
                    images.append({"id":im.id,"numero":im.numero,"url":"https://backend.relwende.com/produitImagesMultiple/"+str(f.id)+"/"+str(im.numero)
                    })
                
                    
                produits.append({"id":f.id,"reference":f.reference,"libele":f.libele,"description":f.description,"stock":f.stock,"idCategorie":f.categorie,"libeleCategorie":categorie.libele,"couleur":f.couleur,"prix":f.prix,"prixReduit":f.prixReduit,"typeEmballage":f.typeEmballage,"images":images})


            retour={"code":200,"title":"Liste des produits","contenu":produits}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode GET"}
      return make_response(jsonify(retour),403)




@app.route('/images' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getProduitImages():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='GET':
            produits=[]
            produit = ImageModel.query.all()
            #user=db.session.query(User).all()

            for f in produit:
                #print(f.description)
                p=db.session.query(Produit).filter(Produit.id==f.produit).first()   
                if p:
                    
                    produits.append({"id":f.id,"reference":p.reference,"produit":p.libele,"produitID":f.produit,"numero":f.numero,"url":"https://backend.relwende.com/produitImagesMultiple/"+str(p.id)+"/"+str(f.numero),"image":f.image})


            retour={"code":200,"title":"Liste des images produits","contenu":produits}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode GET"}
      return make_response(jsonify(retour),403)


@app.route('/delete/image' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def delete_image():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(ImageModel).filter(ImageModel.id==id).first()
            if user1:
                ImageModel.query.filter_by(id=id).delete()
                db.session.commit()

                retour={"code":200,"title":"Suppression du image","contenu":"Image supprimée avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Produit non trouvé"}
                return make_response(jsonify(retour),401)




    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)





@app.route('/delete/produit' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def delete_produit():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(Produit).filter(Produit.id==id).first()
            if user1:
                Produit.query.filter_by(id=id).delete()
                db.session.commit()

                retour={"code":200,"title":"Suppression du produit","contenu":"Produit supprimé avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Produit non trouvé"}
                return make_response(jsonify(retour),401)




    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)



@app.route('/update/produit' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def update_produit():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])
            libele=data['libele']
            reference=data['reference']
            stock=int(data['stock'])
            categorie=int(data['categorie'])
            prix=int(data['prix'])
            prixReduit=int(data['prixReduit'])
            description=data['description']



            user1=db.session.query(Produit).filter(Produit.id==id).first()
            if user1:
                user1.libele=libele
                user1.reference=reference
                user1.stock=stock
                user1.categorie=categorie
                user1.prix=prix
                user1.prixReduit=prixReduit
                user1.description=description
                db.session.add(user1)
                db.session.commit()

                if "typeEmballage" in data:
                    user1.typeEmballage=data["typeEmballage"]
                    db.session.add(user1)
                    db.session.commit()

                if "couleur" in data:
                    user1.couleur=data["couleur"]
                    db.session.add(user1)
                    db.session.commit()


                retour={"code":200,"title":"Modification d'un produit","contenu":"Produit modifié avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de modification","contenu":"Produit non trouvé"}
                return make_response(jsonify(retour),401)




    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/saveProduitImage/<id>', methods=['GET', 'POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def upload_file(id):
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'image' not in request.files:
            #flash('No file part')
             retour={"code":401,"title":"Fichier inconnu","contenu":"Fichier inconnu"}
             return make_response(jsonify(retour),401)
        file = request.files['image']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
           retour={"code":401,"title":"Fichier non selectionné","contenu":"Fichier inconnu"}
           return make_response(jsonify(retour),401)
        if file and allowed_file(file.filename):
            print(file.filename)
            #filename = secure_filename(file.filename)
            file.save(os.path.join(MYDIR + "/" + app.config['UPLOAD_FOLDER']+"/produits", file.filename))
            #return redirect(url_for('download_file', name=filename))
            
            ims=[]
            im=db.session.query(ImageModel).filter(ImageModel.produit==id)
            for img in im:
                ims.append({"id":img.id})
            
            if len(ims)==0:
                user1=ImageModel(file.filename,id,1)
               # user1.image=file.filename
                db.session.add(user1)
                db.session.commit()
                
            else:
                user1=ImageModel(file.filename,id,len(ims)+1)
               # user1.image=file.filename
                db.session.add(user1)
                db.session.commit()
          
                

            retour={"code":200,"title":"Fichier chargé","contenu":"Fichier chargé"}
            return make_response(jsonify(retour),200)



@app.route('/saveLocationImage', methods=['GET', 'POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def upload_fileLocation():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'image' not in request.files:
            #flash('No file part')
             retour={"code":401,"title":"Fichier inconnu","contenu":"Fichier inconnu"}
             return make_response(jsonify(retour),401)
        file = request.files['image']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
           retour={"code":401,"title":"Fichier non selectionné","contenu":"Fichier inconnu"}
           return make_response(jsonify(retour),401)
        if file and allowed_file(file.filename):
            print(file.filename)
            #filename = secure_filename(file.filename)
            file.save(os.path.join(MYDIR + "/" + app.config['UPLOAD_FOLDER']+"/locations", file.filename))
            #return redirect(url_for('download_file', name=filename))
            
            
                
            user1=LocationImageModel(file.filename)
           # user1.image=file.filename
            db.session.add(user1)
            db.session.commit()

            retour={"code":200,"title":"Fichier chargé","contenu":"Fichier chargé"}
            return make_response(jsonify(retour),200)




@app.route('/saveDistributionImage', methods=['GET', 'POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def upload_fileDistribution():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'image' not in request.files:
            #flash('No file part')
             retour={"code":401,"title":"Fichier inconnu","contenu":"Fichier inconnu"}
             return make_response(jsonify(retour),401)
        file = request.files['image']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
           retour={"code":401,"title":"Fichier non selectionné","contenu":"Fichier inconnu"}
           return make_response(jsonify(retour),401)
        if file and allowed_file(file.filename):
            print(file.filename)
            #filename = secure_filename(file.filename)
            file.save(os.path.join(MYDIR + "/" + app.config['UPLOAD_FOLDER']+"/distributions", file.filename))
            #return redirect(url_for('download_file', name=filename))
            
            
                
            user1=DistributionImageModel(file.filename)
           # user1.image=file.filename
            db.session.add(user1)
            db.session.commit()

            retour={"code":200,"title":"Fichier chargé","contenu":"Fichier chargé"}
            return make_response(jsonify(retour),200)



@app.route('/delete/locationImage' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def delete_location_image():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(LocationImageModel).filter(DistributionImageModel.id==id).first()
            if user1:
                LocationImageModel.query.filter_by(id=id).delete()
                db.session.commit()

                retour={"code":200,"title":"Suppression d'image","contenu":"Image supprimée avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Compte non trouvé"}
                return make_response(jsonify(retour),401)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)




@app.route('/delete/distributionImage' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def delete_distribution_image():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(DistributionImageModel).filter(DistributionImageModel.id==id).first()
            if user1:
                DistributionImageModel.query.filter_by(id=id).delete()
                db.session.commit()

                retour={"code":200,"title":"Suppression d'image","contenu":"Image supprimée avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Compte non trouvé"}
                return make_response(jsonify(retour),401)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)


@app.route('/locationVisuel' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getLocationVisuel():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='GET':
            clients=[]
            client = LocationImageModel.query.all()
            #user=db.session.query(User).all()

            for f in client:
                #print(u.nom)
                clients.append({"id":f.id,"nom":f.image,"url":"https://backend.relwende.com/locationImages/"+str(f.id)})


            retour={"code":200,"title":"Liste des images","contenu":clients}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode GET"}
      return make_response(jsonify(retour),403)


@app.route('/distributionVisuel' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getDistributionVisuel():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='GET':
            clients=[]
            client = DistributionImageModel.query.all()
            #user=db.session.query(User).all()

            for f in client:
                #print(u.nom)
                clients.append({"id":f.id,"nom":f.image,"url":"https://backend.relwende.com/distributionImages/"+str(f.id)})


            retour={"code":200,"title":"Liste des images","contenu":clients}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode GET"}
      return make_response(jsonify(retour),403)




@app.route('/produitImagesMultiple/<id>/<numero>' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=False, methods=['GET', 'POST', 'OPTIONS'], headers=['Content-Type'])
def getImage(id,numero):
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='GET':

            user1=db.session.query(ImageModel).filter(ImageModel.produit==int(id)).filter(ImageModel.numero==int(numero)).first()
            if user1:
                return send_file(MYDIR +"/images/produits/"+user1.image, as_attachment=True)

            else:
                retour={"code":404,"title":"NotFound","contenu":"Produit non trouvé"}
                return send_file(MYDIR+"/images/produits/volta.jpeg", as_attachment=True)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)





@app.route('/produitImagess/<id>' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=False, methods=['GET', 'POST', 'OPTIONS'], headers=['Content-Type'])
def getImage22(id):
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='GET':

            user1=db.session.query(ImageModel).filter(ImageModel.produit==int(id)).first()
            if user1:
                return send_file(MYDIR +"/images/produits/"+user1.image, as_attachment=True)

            else:
                retour={"code":404,"title":"NotFound","contenu":"Produit non trouvé"}
                return send_file(MYDIR+"/images/produits/volta.jpeg", as_attachment=True)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)
      
      
@app.route('/produitImages/<id>', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=False,
              methods=['GET', 'POST', 'OPTIONS'], headers=['Content-Type'])
def getImage2(id):
    if request.method == 'OPTIONS':
        return make_response('', 200)

    if request.method == 'GET':
        # Chercher l'image dans la DB
        user1 = db.session.query(ImageModel).filter(ImageModel.produit == int(id)).first()
        
        # Définir le chemin du fichier par défaut
        default_image = os.path.join(MYDIR, "images/produits/volta.jpeg")
        
        if user1:
            image_path = os.path.join(MYDIR, "images/produits", user1.image)
            # Vérifier si le fichier existe physiquement
            if os.path.isfile(image_path):
                return send_file(image_path, as_attachment=True)
            else:
                # Retourner image par défaut si fichier manquant
                return send_file(default_image, as_attachment=True)
        else:
            # Aucun enregistrement DB → image par défaut
            return send_file(default_image, as_attachment=True)

    # Méthode non autorisée
    retour = {"code": 403, "title": "Methode non authorisée",
              "contenu": "Cet endpoint accepte que la methode GET"}
    return make_response(jsonify(retour), 403)


@app.route('/locationImages/<id>' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=False, methods=['GET', 'POST', 'OPTIONS'], headers=['Content-Type'])
def getImageLocation(id):
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='GET':

            user1=db.session.query(LocationImageModel).filter(LocationImageModel.id==int(id)).first()
            if user1:
                return send_file(MYDIR +"/images/locations/"+user1.image, as_attachment=True)

            else:
                retour={"code":404,"title":"NotFound","contenu":"Image non trouvé"}
                return send_file(MYDIR+"/images/produits/volta.jpeg", as_attachment=True)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)
      
      
@app.route('/distributionImages/<id>' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=False, methods=['GET', 'POST', 'OPTIONS'], headers=['Content-Type'])
def getImageDistribution(id):
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='GET':

            user1=db.session.query(DistributionImageModel).filter(DistributionImageModel.id==int(id)).first()
            if user1:
                return send_file(MYDIR +"/images/distributions/"+user1.image, as_attachment=True)

            else:
                retour={"code":404,"title":"NotFound","contenu":"Image non trouvé"}
                return send_file(MYDIR+"/images/produits/volta.jpeg", as_attachment=True)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)





