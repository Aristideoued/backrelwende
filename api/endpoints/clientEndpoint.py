from flask import request, jsonify, make_response, send_file

from models.clientModel import Client
from models.panierModel import Panier
from models.commandeModel import Commande
from models.distributionPanierModel import DistributionPanier 
import hashlib
import vonage
import random
import datetime
from api import app,db,auth,authenticate
from flask_cors import cross_origin

@app.route('/userRegister' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def addClient():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':

            data = request.get_json()

            nom=data['nom']
            prenom=data['prenom']
            email=data['email']
            contact=data['contact']
            password=data['password']
            hashed_password = hashlib.sha256((password).encode("ascii")).hexdigest()
            admin2=db.session.query(Client).filter(Client.contact==contact).first()
            if admin2:
                 retour={"code":401,"title":"User exist","contenu":"Echec de creation du compte, un utilisateur existe deja avec ce numero"}
                 return make_response(jsonify(retour),401)
            else:           
                client=Client(nom,prenom,contact,email,hashed_password)
                db.session.add(client)
                db.session.commit()

                taille=0
                total=0
                totalReduit=0
                statut="non validé"
                client=client.id
                produits={"produits":[]}
            

                
                panier=Panier(taille,total,statut,client,produits,totalReduit)
                db.session.add(panier)
                db.session.commit()

                dispanier=DistributionPanier(taille,total,statut,client,produits,totalReduit)
                db.session.add(dispanier)
                db.session.commit()
                retour={"code":200,"title":"Ajout d'un utilisateur","contenu":"Utilisateur ajouté avec succes"}
                return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)



@app.route('/loginUser' ,methods=['GET','POST','OPTIONS'])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def loginUser():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            #print(request.get_json())
            data = request.get_json()

            contact=data['contact']
            password=data['password']
            hashed_password = hashlib.sha256((password).encode("ascii")).hexdigest()
            admin=db.session.query(Client).filter(Client.contact==contact).filter(Client.password==hashed_password).first()
            if admin :
                retour={"code":200,"title":"Connexion","contenu":"Connexion reussie","nom":admin.nom,"prenom":admin.prenom,"id":admin.id,"code":admin.aacces}
                return make_response(jsonify(retour),200)
            else :
                retour={"code":401,"title":"Connexion","contenu":"Echec de connexion, identifiants incorrects"}
                return make_response(jsonify(retour),401)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)


@app.route('/update/user/password' ,methods=['GET','POST','OPTIONS'])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def updateUserPsw():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            #print(request.get_json())
            data = request.get_json()

            contact=data['telephone']
            password=data['password']
            hashed_password = hashlib.sha256((password).encode("ascii")).hexdigest()
            admin=db.session.query(Client).filter(Client.contact==contact).first()
            if admin :
                admin.password=hashed_password
                db.session.add(admin)
                db.session.commit()
                retour={"code":200,"title":"Modification de mot de passe","contenu":"Modification reussie"}
                return make_response(jsonify(retour),200)
            else :
                retour={"code":401,"title":"Modification","contenu":"Echec de modification, contact incorrect"}
                return make_response(jsonify(retour),401)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)


@app.route('/getcode' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def find_user():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            test=False
            data = request.get_json()

            contact=data['telephone']

            user1=db.session.query(Client).filter(Client.contact==contact).first()
            if user1:
                code=str(random.randint(100000, 999999))
                client = vonage.Client(key="3822c71c", secret="ZbH1QM6iDK43W1Nj")
                sms = vonage.Sms(client)
                
                responseData = sms.send_message(
                    {
                        "from": "VonageAPI",  # Le nom ou le numéro de l'expéditeur
                        "to": contact,  # Remplacez par le numéro de téléphone du destinataire
                        "text": "Cher utilisateur,\n\n\nNous avons recu une demande de recuperation de compte associe a ce numero sur RStore. Afin de garantir la securite de votre compte, veuillez utiliser le code de verification ci-dessous pour confirmer votre demande de recuperation :\n\n\nCode de verification : "+code+" \n\n\nVeuillez entrer ce code sur la page de recuperation de compte.\nAssurez vous de ne pas partager ce code avec quiconque. \nSi vous n'avez pas effectue cette demande, veuillez ignorer ce message\nSi vous avez des questions ou des preoccupations, n'hesitez pas a nous contacter a contact@relwende.com.\n\n\nCordialement,\n\nL'equipe RStore",  # Le texte du message
                    }
                )
                
                if responseData["messages"][0]["status"] == "0":
                    
                    instant_present = datetime.datetime.now()

                    instant_present_str = instant_present.strftime("%Y-%m-%d %H:%M:%S")
                    user1.code=code
                    user1.codeTime=instant_present_str
                    db.session.add(user1)
                    db.session.commit()
                    retour={"code":200,"title":"Envoie de code au client","contenu":"Code envoyé avec succès"}
                    return make_response(jsonify(retour),200)
                else:
                    retour={"code":401,"title":"Envoie de code au client","contenu":"Echec d'envoi du code ,veuillez reessayer"}
                    return make_response(jsonify(retour),401)

                
             

                    
           
               
            else :

                retour={"code":401,"title":"Echec","contenu":"Compte non trouvé"}
                return make_response(jsonify(retour),401)




    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)
   

@app.route('/validecode' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def find_user_by_code():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
           
            data = request.get_json()

            contact=data['telephone']
            code=data['code']
            print(code)

            user1=db.session.query(Client).filter(Client.contact==contact).filter(Client.code==code).first()
            
            
            if user1:  
                
                instant_recupere = datetime.strptime(user1.codeTime, "%Y-%m-%d %H:%M:%S")
                
                instant_present = datetime.now()
                difference = instant_present - instant_recupere
                duree_reference = datetime.timedelta(minutes=10)
                
                if difference > duree_reference:
                    
                    retour={"code":401,"title":"Echec","contenu":"Code expiré, reesayer"}
                    
                    return make_response(jsonify(retour),401)  
                    
                else:
                    retour={"code":200,"title":"Verification de code du client","contenu":"Code valide","client":user1.id}
                    return make_response(jsonify(retour),200)
       
            else:
                retour={"code":401,"title":"Echec","contenu":"Code invalide, reesayer"}
                return make_response(jsonify(retour),401)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)


@app.route('/userById' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getClientById():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            clients=[]
            data = request.get_json()

            id=int(data['id'])

            client=db.session.query(Client).filter(Client.id==id)

            for f in client:
                #print(u.nom)
                clients.append({"id":f.id,"nom":f.nom,"prenom":f.prenom,"contact":f.contact,"email":f.email})


            retour={"code":200,"title":"Client "+str(id),"contenu":clients}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)



@app.route('/userByCode' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getClientByCode():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            clients=[]
            data = request.get_json()

            code=int(data['access'])

            f=db.session.query(Client).filter(Client.aacces==code).first()

           
            clients.append({"id":f.id,"nom":f.nom,"prenom":f.prenom,"contact":f.contact,"email":f.email})


            retour={"code":200,"title":"Connexion par code","contenu":clients}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)

@app.route('/revendeur' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getuseCode():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            clients=[]
            data = request.get_json()

            id=int(data['id'])

            f=db.session.query(Client).filter(Client.id==id).first()

           
            if f.aacces is not None:
                
                clients.append({"code":f.aacces})
    
    
                retour={"code":200,"title":"Connexion par code","contenu":clients}
                #print(users[0])
                return make_response(jsonify(retour),200)
                
            else:
                retour={"code":401,"title":"Connexion par code","contenu":"Veuillez contacter l'administrateur pour recevoir un code revendeur"}
                #print(users[0])
                return make_response(jsonify(retour),401)
                

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)



@app.route('/userCode' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getClientCode():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            clients=[]
            data = request.get_json()

            contact=int(data['id'])
            code=str(data['access'])

            client=db.session.query(Client).filter(Client.id==contact).first()
            
            client2=db.session.query(Client).filter(Client.aacces==code).first()

            if client2:
                
                retour={"code":401,"title":"Attribution de code","contenu":"Echec , ce code a été déja attribué à "+client2.prenom+" "+client2.nom}
                return make_response(jsonify(retour),401)

            elif client:
                client.aacces=code
                db.session.add(client)
                db.session.commit()
                retour={"code":200,"title":"Attribution de code","contenu":"Code attribué avec succes"}
                return make_response(jsonify(retour),200)

            else:
                retour={"code":404,"title":"Attribution de code","contenu":"Client non trouvé"}
                return make_response(jsonify(retour),404)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)


@app.route('/users' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getClient():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='GET':
            clients=[]
            client = Client.query.all()
            #user=db.session.query(User).all()

            for f in client:
                #print(u.nom)
                code=""
                if f.aacces is not None:
                    code =f.aacces


                panier=db.session.query(DistributionPanier).filter(DistributionPanier.client==id)

                if panier:
                    pass
                else:
                    newpanier=DistributionPanier(0,0,"non validé",f.id,{"produits":[]},0)
                    db.session.add(newpanier)
                    db.session.commit()

                
                    
                clients.append({"id":f.id,"nom":f.nom,"prenom":f.prenom,"contact":f.contact,"email":f.email,"access":code})


            retour={"code":200,"title":"Liste des clients","contenu":clients}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode GET"}
      return make_response(jsonify(retour),403)


@app.route('/delete/user' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def delete_user():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(Client).filter(Client.id==id).first()
            
            if user1:
                Client.query.filter_by(id=id).delete()
                db.session.commit()
                cmd=db.session.query(Commande).filter(Commande.client==id)
                pnr=db.session.query(Panier).filter(Panier.client==id)
                for cd in cmd:
                    Commande.query.filter_by(id=cd.id).delete()
                    db.session.commit()
                 
                for pn in pnr:
                    Panier.query.filter_by(id=pn.id).delete()
                    db.session.commit()    

                retour={"code":200,"title":"Suppression de compte client","contenu":"Compte supprimé avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Compte non trouvé"}
                return make_response(jsonify(retour),401)




    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)



@app.route('/update/user' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def update_user():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])
            nom=data['nom']
            prenom=data['prenom']
            email=data['email']
            contact=data['contact']



            user1=db.session.query(Client).filter(Client.id==id).first()
            if user1:
                user1.nom=nom
                user1.prenom=prenom
                user1.email=email
                user1.contact=contact
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