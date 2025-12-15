import os
from flask import request, jsonify, send_file, make_response, Blueprint
from models.entreeModel import Entree
from PIL import Image
from api import app,db,auth,authenticate
from flask_cors import cross_origin

UPLOAD_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
MYDIR = os.path.dirname(__file__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/addEntree' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def addEntree():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':

            data = request.get_json()

            libele=data['libele']
            image="defaut"
            
            entree=Entree(libele,image)
            db.session.add(entree)
            db.session.commit()
            retour={"code":200,"title":"Ajout d'une entree","contenu":"Entree ajoutée avec succes"}
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)

@app.route('/entreeById' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getEntreeById():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            entrees=[]
            data = request.get_json()

            id=int(data['id'])

            entree=db.session.query(Entree).filter(Entree.id==id).first()

         
            entrees.append({"id":entree.id,"libele":entree.libele,"image":entree.image})


            retour={"code":200,"title":"Entree "+str(id),"contenu":entrees}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)



@app.route('/entrees' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getEntree():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='GET':
            entrees=[]
            entree = Entree.query.all()
            #user=db.session.query(User).all()

            for f in entree:
                #print(u.nom)
                entrees.append({"id":f.id,"libele":f.libele,"image":f.image})


            retour={"code":200,"title":"Liste des Entrees","contenu":entrees}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode GET"}
      return make_response(jsonify(retour),403)


@app.route('/delete/entree' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def delete_Entree():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(Entree).filter(Entree.id==id).first()
            if user1:                

                Entree.query.filter_by(id=id).delete()
                db.session.commit()

                retour={"code":200,"title":"Suppression d'une Entree et tous ses produits","contenu":"Entree supprimée avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Entree non trouvée"}
                return make_response(jsonify(retour),401)




    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)



@app.route('/update/entree' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def update_Entree():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])
            libele=data['libele']
            



            user1=db.session.query(Entree).filter(Entree.id==id).first()
            if user1:
                user1.libele=libele
                db.session.add(user1)
                db.session.commit()

                retour={"code":200,"title":"Modification d'une Entree","contenu":"Entree modifiée avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de modification","contenu":"Entree non trouvé"}
                return make_response(jsonify(retour),401)




    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/saveEntreeImage/<id>', methods=['GET', 'POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def upload_file_entre(id):
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
            file.save(os.path.join(MYDIR + "/" + app.config['UPLOAD_FOLDER']+"/entrees", file.filename))
            #return redirect(url_for('download_file', name=filename))
            user1=db.session.query(Entree).filter(Entree.id==id).first()
            user1.image=file.filename
            db.session.add(user1)
            db.session.commit()

            retour={"code":200,"title":"Fichier chargé","contenu":"Fichier chargé"}
            return make_response(jsonify(retour),200)


@app.route('/entreeImages/<id>' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=False, methods=['GET', 'POST', 'OPTIONS'], headers=['Content-Type'])
def getImageCatEntre(id):
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='GET':

            user1=db.session.query(Entree).filter(Entree.id==id).first()
            if user1:
                return send_file(MYDIR+"/images/entrees/"+user1.image, as_attachment=True)

            else:
                retour={"code":404,"title":"NotFound","contenu":"Alert non trouvée"}
                return send_file(MYDIR+"/images/produits/volta.jpeg", as_attachment=True)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)
