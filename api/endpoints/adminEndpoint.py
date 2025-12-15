from flask import request, jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from api import app,db,auth,authenticate
from models.adminModel import Admin
import hashlib
from flask_cors import cross_origin

@app.route('/admins' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getadmins():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='GET':
            admins=[]
            admin = Admin.query.all()
            #user=db.session.query(User).all()

            for u in admin:
                #print(u.nom)
                admins.append({"id":u.id,"nom":u.nom,"prenom":u.prenom,"email":u.username})


            retour={"code":200,"title":"Liste des admins","contenu":admins}
            #print(users[0])
            return make_response(jsonify(retour),200)


    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode GET"}
      return make_response(jsonify(retour),403)




@app.route('/update/adminPassword' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def update_admin_password():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])

            password=data['password']
            hashed_password = hashlib.sha256((password).encode("ascii")).hexdigest()
            user1=db.session.query(Admin).filter(Admin.id==id).first()
            if user1:
                user1.password=hashed_password
                db.session.add(user1)
                db.session.commit()

                retour={"code":200,"title":"Modification de mot de passe admin","contenu":"Mot de passe modifié avec succès"}
                return make_response(jsonify(retour),200)

            else :

                retour={"code":401,"title":"Echec de modification","contenu":"Compte non trouvé"}
                return make_response(jsonify(retour),401)





    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)



@app.route('/update/admin' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def update_admin():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])
            nom=data['nom']
            prenom=data['prenom']
            email=data['username']

            password=data['password']
            hashed_password=''
            if password!='':
               hashed_password = hashlib.sha256((password).encode("ascii")).hexdigest()



            user1=db.session.query(Admin).filter(Admin.id==id).first()
            if user1 and hashed_password=='':
                user1.nom=nom
                user1.prenom=prenom
                user1.username=email
                db.session.add(user1)
                db.session.commit()

                retour={"code":200,"title":"Modification de compte","contenu":"Compte modifié avec succès"}
                return make_response(jsonify(retour),200)
            elif user1 and hashed_password!='':
                user1.nom=nom
                user1.prenom=prenom
                user1.username=email
                user1.password=hashed_password
                db.session.add(user1)
                db.session.commit()

                retour={"code":200,"title":"Modification de compte","contenu":"Compte modifié avec succès"}
                return make_response(jsonify(retour),200)
    

            else :

                retour={"code":401,"title":"Echec de modification","contenu":"Compte non trouvé"}
                return make_response(jsonify(retour),401)





    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)




@app.route('/adminById' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getAdminById():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            admins=[]
            data = request.get_json()

            id=int(data['id'])

            admin=db.session.query(Admin).filter(Admin.id==id).first()

         
            admins.append({"id":admin.id,"nom":admin.nom,"prenom":admin.prenom,"username":admin.username})


            retour={"code":200,"title":"Admin "+str(id),"contenu":admins}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)




#@auth.login_required
@app.route('/delete/admin' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def delete_admin():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(Admin).filter(Admin.id==id).first()
            if user1:
                Admin.query.filter_by(id=id).delete()
                db.session.commit()

                retour={"code":200,"title":"Suppression de compte","contenu":"Compte supprimé avec succès"}
                return make_response(jsonify(retour),200)

            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Compte non trouvé"}
                return make_response(jsonify(retour),401)





    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)








#@auth.login_required
@app.route('/login2' ,methods=['POST',"OPTIONS"])
@auth.login_required
def login2():
    
    if request.method=='POST':
            #print(request.get_json())
            data = request.get_json()

            username=data['username']
            password=data['password']
            hashed_password = hashlib.sha256((password).encode("ascii")).hexdigest()
            admin=db.session.query(Admin).filter(Admin.password==hashed_password).first()
            admin2=db.session.query(Admin).filter(Admin.username==username).first()
            if admin and admin2:
                retour={"code":200,"title":"Connexion","contenu":"Connexion reussie","nom":admin2.prenom,"username":admin2.username}
                return make_response(jsonify(retour),200)

            else :
                retour={"code":401,"title":"Connexion","contenu":"Echec de connexion, identifiants incorrects"}
                return make_response(jsonify(retour),401)


    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)

@app.route('/login', methods=['POST', 'OPTIONS'])  # Ajoutez OPTIONS ici
@auth.login_required
def login():
    # Gérer la requête OPTIONS (preflight)
    if request.method == 'OPTIONS':
        return make_response('', 200)
    
    if request.method == 'POST':
        # Votre code existant...
        data = request.get_json()
        username = data['username']
        password = data['password']
        hashed_password = hashlib.sha256((password).encode("ascii")).hexdigest()
        admin = db.session.query(Admin).filter(Admin.password==hashed_password).first()
        admin2 = db.session.query(Admin).filter(Admin.username==username).first()
        if admin and admin2:
            retour = {"code":200,"title":"Connexion","contenu":"Connexion reussie","nom":admin2.prenom,"username":admin2.username}
            return make_response(jsonify(retour), 200)
        else:
            retour = {"code":401,"title":"Connexion","contenu":"Echec de connexion, identifiants incorrects"}
            return make_response(jsonify(retour), 401)


@app.route('/registerAdmin' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def registerAdmin():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            test=False
            data = request.get_json()

            nom=data['nom']
            prenom=data['prenom']
            username=data['username']
            password=data['password']
            hashed_password = hashlib.sha256((password).encode("ascii")).hexdigest()
            user1=db.session.query(Admin).filter(Admin.username==username).first()
            if user1:
                retour={"code":401,"title":"Echec de creation de compte","contenu":"Ce username est deja associé à un compte"}
                return make_response(jsonify(retour),401)

            else :
                user=Admin(nom,prenom,username,hashed_password)
                db.session.add(user)
                db.session.commit()
                retour={"code":200,"title":"Creation de compte","contenu":"Compte crée avec succes"}
                return make_response(jsonify(retour),200)


    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)
