import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import request, jsonify, make_response
from api import app,db,auth,authenticate
from models.commandeModel import Commande
from models.clientModel import Client
from datetime import datetime
import hashlib
from flask_cors import cross_origin

@app.route('/addCommande' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def addCommande():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':

            data = request.get_json()

           
            date=data['date']
            produits1=data['produits']
            client=int(data['client'])
            heure=data['heure']
            addresseLivraison=data['addresseLivraison']
            libele=data['libele']
            dateLivraisonSouhaite=data['dateLivraisonSouhaite']

            quantite=len(produits1)
            dateLivraison=data['dateLivraison']
            dateEvenement=data['dateEvenement']
            dureeLocation=int(data['dureeLocation'])
            
            heureLivraison=""
           
            statut="En cours"
            prod=[]
            produits={}

            total=0
            totalReduit=0
            for i in range(0,len(produits1)):
                prod.append(produits1[i])
                total+=produits1[i]["prix"]
                totalReduit+=produits1[i]["prixReduit"]

            produits["produits"]=prod   
            produits["total"]=total
            produits["totalReduit"]=totalReduit

            
            commande=Commande(dureeLocation,quantite,date,dateEvenement,dateLivraison,dateLivraisonSouhaite,heure,heureLivraison,addresseLivraison,libele,statut,produits,client)
            db.session.add(commande)
            db.session.commit()
            retour={"code":200,"title":"Ajout d'une commande","contenu":"Commande ajoutée avec succes"}
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)


@app.route('/commandeById' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getCommandeById():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            commandes=[]
            data = request.get_json()

            id=int(data['id'])

            commande=db.session.query(Commande).filter(Commande.id==id)

            for f in commande:
                #print(u.nom)
                client=db.session.query(Client).filter(Client.id==f.client).first()
                commandes.append({"id":f.id,"dateLivraisonSouhaite":f.dateLivraisonSouhaite,"dateEvenement":f.dateEvenement,"dureeLocation":f.dureeLocation,"quantite":f.quantite,"date":f.date,"client":{"nom":client.nom,"prenom":client.prenom,"contact":client.contact,"id":client.id,"revendeur":client.aacces},"dateLivraison":f.dateLivraison,"dateLivraisonSouhaite":f.dateLivraisonSouhaite,"heure":f.heure,"heureLivraison":f.heureLivraison,"addresseLivraison":f.addresseLivraison,"libele":f.libele,"statut":f.statut,"produits":f.produits})


            retour={"code":200,"title":"Commande "+str(id),"contenu":commandes}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)



@app.route('/all/commandes' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getCommandes():
    if request.method == 'OPTIONS':
        response= make_response('', 200)
        return response
    if request.method=='GET':
            commandes=[]
            commande = Commande.query.all()
            #user=db.session.query(User).all()

            for f in commande:
                #print(u.nom)
                client=db.session.query(Client).filter(Client.id==f.client).first()
                
                if client:
                    commandes.append({"id":f.id,"dateEvenement":f.dateEvenement,"dureeLocation":f.dureeLocation, "dateLivraisonSouhaite":f.dateLivraisonSouhaite, "quantite":f.quantite,"date":f.date,"client":{"nom":client.nom,"prenom":client.prenom,"contact":client.contact,"id":client.id,"revendeur":client.aacces},"dateLivraison":f.dateLivraison,"heure":f.heure,"heureLivraison":f.heureLivraison,"addresseLivraison":f.addresseLivraison,"libele":f.libele,"statut":f.statut,"produits":f.produits})

            x=list(reversed(commandes))
            retour={"code":200,"title":"Liste des commandes","contenu":x}
            #print(users[0])
            response= make_response(jsonify(retour),200)
            return response

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode GET"}
      return make_response(jsonify(retour),403)




@app.route('/commandes', methods=['GET', 'POST', 'OPTIONS'])
@auth.login_required
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
def getCommande():
    if request.method == 'OPTIONS':
        # Réponse preflight
        response = make_response('', 200)
        return response

    if request.method == 'GET':
        commandes = []
        for f in Commande.query.all():
            client = db.session.query(Client).filter(Client.id == f.client).first()
            if client:
                commandes.append({
                    "id": f.id,
                    "dateEvenement": f.dateEvenement,
                    "dureeLocation": f.dureeLocation,
                    "dateLivraisonSouhaite": f.dateLivraisonSouhaite,
                    "quantite": f.quantite,
                    "date": f.date,
                    "client": {"nom": client.nom, "prenom": client.prenom, "contact": client.contact, "id": client.id,"revendeur":client.aacces},
                    "dateLivraison": f.dateLivraison,
                    "heure": f.heure,
                    "heureLivraison": f.heureLivraison,
                    "addresseLivraison": f.addresseLivraison,
                    "libele": f.libele,
                    "statut": f.statut,
                    "produits": f.produits
                })

        x = list(reversed(commandes))
        retour = {"code": 200, "title": "Liste des commandes", "contenu": x}
        response = make_response(jsonify(retour), 200)
        return response

    # Méthode non autorisée
    retour = {"code": 403, "title": "Methode non authorisée", "contenu": "Cet endpoint accepte que la methode GET"}
    return make_response(jsonify(retour), 403)



@app.route('/delete/commande' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def delete_commande():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(Commande).filter(Commande.id==id).first()
            if user1:
                Commande.query.filter_by(id=id).delete()
                db.session.commit()
                us=db.session.query(Client).filter(Client.id==user1.client).first()
                destinataire ="relwendestore@gmail.com"
    
                expediteur= "contact@relwende.com"
                sujet = "Annulation d'une commande"
                message = MIMEMultipart()
                message['From'] = expediteur
                message['To'] = destinataire
                message['Subject'] = sujet
                corps_du_message = us.nom+" "+us.prenom+" a annulé sa commande, rendez-vous sur https://admin.relwende.com pour plus de details"
                message.attach(MIMEText(corps_du_message, 'plain'))
                serveur_smtp = "mail.relwende.com"
                port_smtp = 465
                nom_utilisateur = "contact@relwende.com"
                mot_de_passe = "2885351Landry12@"
                s = smtplib.SMTP_SSL(host='mail.relwende.com', port=465)
                s.login(nom_utilisateur, mot_de_passe)
                texte = message.as_string()
                s.sendmail(expediteur, destinataire, texte)
                s.quit()

                retour={"code":200,"title":"Suppression de  Commande","contenu":"Commande supprimée avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Commande non trouvée"}
                return make_response(jsonify(retour),401)




    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)



@app.route('/update/commande' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def update_commande():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            #test=False
            data = request.get_json()

            id=int(data['id'])
            quantite=int(data['quantite'])
            #date=data['date']
            #heure=data['heure']
            dateLivraison=data['dateLivraison']
            dureeLocation=data['dureeLocation']
            dateEvenement=data['dateEvenement']
            heureLivraison=data['heureLivraison']
            addresseLivraison=data['addresseLivraison']
            libele=data['libele']
            statut=data['statut']
            #produits=data['produits']
            #client=int(data['client'])



            user1=db.session.query(Commande).filter(Commande.id==id).first()
            if user1:
                user1.quantite=quantite
                user1.dateEvenement=dateEvenement
                user1.dureeLocation=dureeLocation
                user1.dateLivraison=dateLivraison
                user1.heureLivraison=heureLivraison
                user1.addresseLivraison=addresseLivraison
                user1.statut=statut
                user1.libele=libele
                db.session.add(user1)
                db.session.commit()

                retour={"code":200,"title":"Modification d'une commande","contenu":"Commande modifiée avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de modification","contenu":"Commande non trouvée"}
                return make_response(jsonify(retour),401)




    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)

@app.route('/commandeByUser' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getCommandeByUser():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            commandes=[]
            data = request.get_json()

            id=int(data['user'])

            commande=db.session.query(Commande).filter(Commande.client==id)
            #client=db.session.query(Client).filter(Client.id==f.client).first()
            
            for f in commande:
                #print(u.nom)
                
                commandes.append({"id":f.id,"dateEvenement":f.dateEvenement,"dureeLocation":f.dureeLocation,"quantite":f.quantite,"date":f.date,"dateLivraison":f.dateLivraison,"heure":f.heure,"heureLivraison":f.heureLivraison,"addresseLivraison":f.addresseLivraison,"dateLivraisonSouhaite":f.dateLivraisonSouhaite, "libele":f.libele,"statut":f.statut,"produits":f.produits})

            if len(commandes)>0:

                retour={"code":200,"title":"Commande du user "+str(id),"contenu":commandes}
                #print(users[0])
                return make_response(jsonify(retour),200)
            else:
                retour={"code":200,"title":"Commande du user "+str(id),"contenu":commandes}
                #print(users[0])
                return make_response(jsonify(retour),200)
    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)
