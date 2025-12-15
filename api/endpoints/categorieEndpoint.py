from flask import request, jsonify, make_response, send_file
from api import app,db,auth,authenticate
from models.categorieModel import Categorie
from models.produitModel import Produit
import os
from flask_cors import cross_origin

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MYDIR = os.path.dirname(__file__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/addCategorie' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def addCategorie():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':

            data = request.get_json()

            libele=data['libele']
            image="defaut"
            
            categorie=Categorie(libele,image)
            db.session.add(categorie)
            db.session.commit()
            retour={"code":200,"title":"Ajout d'une Categorie","contenu":"Categorie ajoutée avec succes"}
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)

@app.route('/categorieById' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getCategorieById():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            categories=[]
            data = request.get_json()

            id=int(data['id'])

            categorie=db.session.query(Categorie).filter(Categorie.id==id).first()

         
            categories.append({"id":categorie.id,"libele":categorie.libele,"image":categorie.image})


            retour={"code":200,"title":"Categorie "+str(id),"contenu":categories}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)



@app.route('/categories' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getCategorie():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='GET':
            categories=[]
            categorie = Categorie.query.all()
            #user=db.session.query(User).all()

            for f in categorie:
                #print(u.nom)
                if f.libele !="BOISSON":
                    
                    categories.append({"id":f.id,"libele":f.libele,"image":f.image})


            retour={"code":200,"title":"Liste des Categories","contenu":categories}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode GET"}
      return make_response(jsonify(retour),403)


@app.route('/all/categories' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getCategorieAll():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='GET':
            categories=[]
            categorie = Categorie.query.all()
            #user=db.session.query(User).all()

            for f in categorie:
                #print(u.nom)
                
                    
                categories.append({"id":f.id,"libele":f.libele,"image":f.image})


            retour={"code":200,"title":"Liste des Categories","contenu":categories}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode GET"}
      return make_response(jsonify(retour),403)


@app.route('/delete/categorie' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def delete_Categorie():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(Categorie).filter(Categorie.id==id).first()
            if user1:
                prod=db.session.query(Produit).filter(Produit.categorie==id)
                for produit in prod:
                    produit.query.filter_by(categorie=id).delete()
                    db.session.commit()

                Categorie.query.filter_by(id=id).delete()
                db.session.commit()

                retour={"code":200,"title":"Suppression d'une Categorie et tous ses produits","contenu":"Categorie supprimée avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Categorie non trouvée"}
                return make_response(jsonify(retour),401)




    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)



@app.route('/update/categorie' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def update_categorie():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])
            libele=data['libele']
            



            user1=db.session.query(Categorie).filter(Categorie.id==id).first()
            if user1:
                user1.libele=libele
                db.session.add(user1)
                db.session.commit()

                retour={"code":200,"title":"Modification d'une Categorie","contenu":"Categorie modifiée avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de modification","contenu":"Categorie non trouvé"}
                return make_response(jsonify(retour),401)




    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/saveCategorieImage/<id>', methods=['GET', 'POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def upload_file_cat(id):
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
            file.save(os.path.join(MYDIR + "/" + app.config['UPLOAD_FOLDER']+"/categories", file.filename))
            #return redirect(url_for('download_file', name=filename))
            user1=db.session.query(Categorie).filter(Categorie.id==id).first()
            user1.image=file.filename
            db.session.add(user1)
            db.session.commit()

            retour={"code":200,"title":"Fichier chargé","contenu":"Fichier chargé"}
            return make_response(jsonify(retour),200)


@app.route('/categorieImagess/<id>' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=False, methods=['GET', 'POST', 'OPTIONS'], headers=['Content-Type'])
def getImageCatss(id):
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='GET':

            user1=db.session.query(Categorie).filter(Categorie.id==id).first()
            if user1 and user1.image !="defaut":
                return send_file(MYDIR+"/images/categories/"+user1.image, as_attachment=True)

            else:
                retour={"code":404,"title":"NotFound","contenu":"Categorie non trouvée"}
                return send_file(MYDIR+"/images/produits/volta.jpeg", as_attachment=True)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)
      
      
      
@app.route('/categorieImages/<id>', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=False,
              methods=['GET', 'POST', 'OPTIONS'], headers=['Content-Type'])
def getImageCat(id):
    if request.method == 'OPTIONS':
        return make_response('', 200)

    if request.method == 'GET':
        # Chercher la catégorie dans la DB
        cat = db.session.query(Categorie).filter(Categorie.id == id).first()
        
        # Chemin de l'image par défaut
        default_image = os.path.join(MYDIR, "images/produits/volta.jpeg")
        
        if cat and cat.image != "defaut":
            image_path = os.path.join(MYDIR, "images/categories", cat.image)
            if os.path.isfile(image_path):
                return send_file(image_path, as_attachment=True)
            else:
                # Fichier manquant → image par défaut
                return send_file(default_image, as_attachment=True)
        else:
            # Catégorie non trouvée → image par défaut
            return send_file(default_image, as_attachment=True)

    # Méthode non autorisée
    retour = {"code": 403, "title": "Methode non authorisée",
              "contenu": "Cet endpoint accepte que la methode GET"}
    return make_response(jsonify(retour), 403)
      
      