from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from flask import Blueprint, jsonify, request, make_response
from models.categorieModel import Categorie
from models.commandeModel import Commande
from models.panierModel import Panier
from models.clientModel import Client
from models.produitModel import Produit
from api import app,db,auth,authenticate
from flask_cors import cross_origin

@app.route('/addPanier' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def addPanier():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':

            data = request.get_json()

            taille=0
            total=0
            totalReduit=0
            statut="non validé"
            client=int(data['client'])
            produits={"produits":[]}
          

            
            panier=Panier(taille,total,statut,client,produits,totalReduit)
            db.session.add(panier)
            db.session.commit()
            retour={"code":200,"title":"Ajout d'un Panier","contenu":"Panier ajoutée avec succes"}
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)


@app.route('/panierById' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getPanierById():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            paniers=[]
            data = request.get_json()

            id=int(data['id'])

            panier=db.session.query(Panier).filter(Panier.id==id)

            for f in panier:
                #print(u.nom)
                client=db.session.query(Client).filter(Client.id==f.client).first()
                paniers.append({"id":f.id,"taille":f.taille,"total":f.total,"statut":f.statut,"client":{"nom":client.nom,"prenom":client.prenom,"contact":client.contact,"id":client.id},"produits":f.produits["produits"],"totalReduit":f.totalReduit})


            retour={"code":200,"title":"Panier "+str(id),"contenu":paniers}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)




@app.route('/panierByUser' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getPanierByUser():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            paniers=[]
            data = request.get_json()

            id=int(data['clientId'])

            panier=db.session.query(Panier).filter(Panier.client==id)

            for f in panier:
                #print(u.nom)
                tr=0
                if f.total==0:
                    f.totalReduit=0
                    db.session.add(f)
                    db.session.commit()
                    
                paniers.append({"id":f.id,"taille":f.taille,"total":f.total,"statut":f.statut,"produits":f.produits,"totalReduit":f.totalReduit})


            retour={"code":200,"title":"Panier du client "+str(id),"contenu":paniers}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode POST"}
      return make_response(jsonify(retour),403)





@app.route('/paniers' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def getPanier():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='GET':
            paniers=[]
            panier = Panier.query.all()
            #user=db.session.query(User).all()

            for f in panier:
                #print(type(f.client))
                client=db.session.query(Client).filter(Client.id==f.client).first() 
                if client:
                    
                    paniers.append({"id":f.id,"taille":f.taille,"total":f.total,"statut":f.statut,"client":{"nom":client.nom,"prenom":client.prenom,"contact":client.contact,"id":client.id},"produits":f.produits,"totalReduit":f.totalReduit})
                   
                    
  
            retour={"code":200,"title":"Liste des Paniers","contenu":paniers}
            #print(users[0])
            return make_response(jsonify(retour),200)

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode GET"}
      return make_response(jsonify(retour),403)


@app.route('/delete/panier' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def delete_Panier():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])

            user1=db.session.query(Panier).filter(Panier.id==id).first()
            if user1:
                Panier.query.filter_by(id=id).delete()
                db.session.commit()

                retour={"code":200,"title":"Suppression de  Panier","contenu":"Panier supprimée avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de suppression","contenu":"Panier non trouvée"}
                return make_response(jsonify(retour),401)




    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)





@app.route('/update/panier/totalReduit' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def update_Paniers():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='GET':
            
            panier = Panier.query.all()
            
            for p in panier:
                p.totalReduit=0
                db.session.add(p)
                db.session.commit()
                
                
            retour={"code":200,"title":"Modification d'une Panier","contenu":"Panier modifiée avec succès"}
            return make_response(jsonify(retour),200)
            

    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)



@app.route('/update/panier' ,methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def update_Panier():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
            test=False
            data = request.get_json()

            id=int(data['id'])
            total=int(data['total'])
            totalReduit=int(data['totalReduit'])
            statut=data['statut']
            



            user1=db.session.query(Panier).filter(Panier.id==id).first()
            if user1:
                user1.total=total
                user1.totalReduit=totalReduit
                user1.statut=statut
                db.session.add(user1)
                db.session.commit()

                retour={"code":200,"title":"Modification d'une Panier","contenu":"Panier modifiée avec succès"}
                return make_response(jsonify(retour),200)
            else :

                retour={"code":401,"title":"Echec de modification","contenu":"Compte non trouvé"}
                return make_response(jsonify(retour),401)




    else:
      retour={"code":403,"title":"Methode non authorisée","contenu":"Cet endpoint accepte que la methode post"}
      return make_response(jsonify(retour),403)



@app.route('/cart/update', methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def cart_update_new():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method=='POST':
        data = request.get_json()            
        unicode = int(data["product"])
        user = int(data["user"])
        cart=db.session.query(Panier).filter(Panier.client==user).first()
        #cart = CartModel.objects(user=user.get("username")).first()
        #devise = DeviseModel.objects()[0]
        cart_payload =db.session.query(Produit).filter(Produit.id==int(unicode)).first()
        #print("<======================>")
        #print("id ::: ",cart_payload)
        #print("<======================>")
        if cart:
            print(cart)
            if len(cart.produits["produits"])>0:
                productToAdd=None

                for product in cart.produits['produits']:
                    if product['id']==cart_payload.id:
                        productToAdd=product

                if productToAdd is not None:
                    #print(productToAdd)
                    position = cart.produits['produits'].index(productToAdd)
                    print("position :::: ",position)
                    index=productToAdd['index']
                    
                    l=list(cart.produits['produits'])
                    l[position]['index']=productToAdd['index']+1
                    l[position]['prix']=productToAdd['prix']+cart_payload.prix
                    l[position]['prixReduit']=productToAdd['prixReduit']+cart_payload.prixReduit
                    #print("l apres ajout ::::= ",l[position])
                    cart.produits={"produits":[]}
                    db.session.add(cart)
                    db.session.commit()
                    cart.produits={"produits":l}
                    #cart.produits['produits'][position]['index']=productToAdd['index']+1
                    #cart.produits['produits'][position]['prix']=productToAdd['prix']+cart_payload.prix
                    cart.statut="En cours"
                    cart.taille=cart.taille+1
                    cart.total=cart.total+cart_payload.prix
                    cart.totalReduit=cart.totalReduit+cart_payload.prixReduit
                    db.session.add(cart)
                    db.session.commit()
                    retour={"title":"cart  updated","contenu":"Ajout au panier reussi","code":200}
                    return make_response(jsonify(retour),200)
                

                else:
                    cart_payload.index=1
                    l=list(cart.produits['produits'])
                    l.append(cart_payload.extended())
                    print("l===",len(l))           
                    cart.produits={"produits":l}
                    cart.taille=cart.taille+1
                    cart.total=cart.total+cart_payload.prix
                    cart.totalReduit=cart.totalReduit+cart_payload.prixReduit
                    cart.statut="En cours"
                    db.session.add(cart)
                    db.session.commit()
                    retour={"title":"cart  updated","contenu":"Ajout au panier reussi","code":200}
                    return make_response(jsonify(retour),200)
            else:
                cart_payload.index=1
                l=list(cart.produits['produits'])
                l.append(cart_payload.extended())
                print("len l===",len(l))
                cart.produits={"produits":l}
                cart.taille=cart.taille+1
                cart.statut="En cours"
                cart.total=cart.total+cart_payload.prix
                cart.totalReduit=cart.totalReduit+cart_payload.prixReduit
                db.session.add(cart)
                db.session.commit()
                retour={"title":"cart  updated","contenu":"Ajout au panier reussi","code":200}
                return make_response(jsonify(retour),200)


            
            #cart.save()
            
        else:
            retour={"title":"cart not  updated","contenu":"Panier non trouvé","code":404}
            return make_response(jsonify(retour),404)    
    else:
        retour={"title":"Méthode Non Authorisée","contenu":"Cette interface n'accepte que la méthode POST.","code":405}
        return make_response(jsonify(retour),405)


@app.route('/cart/product/purge', methods=['GET','POST',"OPTIONS"])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def cart_purge():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method == 'POST':
        
           
                if request.data:
                    data = request.get_json()  
                    #data = json.loads(fk.request.data)
                    #cart_payload = data["product"]
                   
                    unicode = int(data["product"])
                    user = int(data["user"])
                    cart=db.session.query(Panier).filter(Panier.client==user).first()
                    productToRemove=None
                    print(cart.produits['produits'])
                    for product in cart.produits['produits']:
                        print(product)
                        if int(product['id'])==unicode:
                            productToRemove=product
                    if productToRemove is not None:
                        print(productToRemove)
                        l=list(cart.produits['produits'])
                        l.remove(productToRemove)
                        cart.produits={"produits":[]}
                        db.session.add(cart)
                        db.session.commit()
                        cart.produits={"produits":l}
                        cart.taille=cart.taille-int(productToRemove['index'])
                        cart.total=cart.total-int(productToRemove['prix'])
                        cart.totalReduit=cart.totalReduit-int(productToRemove['prixReduit'])
                        db.session.add(cart)
                        db.session.commit()

                        retour={"title":"Suppression reussie","contenu":"Produit supprimé du panier avec success","code":200}
                        return make_response(jsonify(retour),200)
                        




                    else:
                        retour={"title":"Produit non trouvé","contenu":"Produit non trouvé dans le panier","code":404}
                        return make_response(jsonify(retour),404)
                else:
                    retour={"title":"Données non trouvées","contenu":"Paramètres manquants","code":500}
                    return make_response(jsonify(retour),500)
           
    else:
        retour={"title":"Méthode Non Authorisée","contenu":"Cette interface n'accepte que la méthode POST.","code":405}
        return make_response(jsonify(retour),405)






@app.route('/cart/product/quantite', methods=['GET','POST','PUT','UPDATE','DELETE','POST', 'OPTIONS'])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def quantite_product_in_cart():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method == 'POST':         
                if request.data:
                    data = request.get_json()
                    unicode = int(data["product"])
                    user = int(data["user"])
                    quantite = int(data["quantite"])
                    cart=db.session.query(Panier).filter(Panier.client==user).first()
                    productToIncrement=None
                    for product in cart.produits['produits']:
                        if int(product['id'])==unicode:
                            productToIncrement=product
                    if productToIncrement:
                        #print(productToIncrement)
                        l=list(cart.produits['produits'])
                        #cart.taille=cart.taille+1
                        #cart.total=cart.total+(int(productToIncrement['prix'])/int(productToIncrement['index']))
                        cart.produits={"produits":[]}
                        cart.total=0
                        cart.totalReduit=0
                        cart.taille=0
                        db.session.add(cart)
                        db.session.commit()
                        
                        for product in l:
                            if int(product['id'])==int(productToIncrement['id']):
                                product['prix']=quantite *(int(product['prix'])/int(product['index']))
                                product['prixReduit']=quantite *(int(product['prixReduit'])/int(product['index']))
                                product['index']=quantite

                        for p in l:
                            cart.total=cart.total+int(p['prix'])
                            cart.totalReduit=cart.totalReduit+int(p['prixReduit'])
                            cart.taille=cart.taille+int(p['index'])
                            db.session.add(cart)
                            db.session.commit()        

                        cart.produits={"produits":l}
                        db.session.add(cart)
                        db.session.commit()

                        retour={"title":"Quantité fixée","contenu":"Quantité fixée dans le panier avec succes.","code":200}
                        return make_response(jsonify(retour),200)
                    
                    else:
                        retour={"title":"Produit non trouvé","contenu":"Produit non trouvé dans le panier.","code":404}
                        return make_response(jsonify(retour),404)
                    
                else:
                    retour={"title":"Données non trouvées","contenu":"Données non trouvées","code":500}
                    return make_response(jsonify(retour),500)
                    
          
    else:
        retour={"title":"Méthode Non Authorisée","contenu":"Cette interface n'accepte que la méthode POST.","code":405}
        return make_response(jsonify(retour),405)



@app.route('/cart/product/increment', methods=['GET','POST','PUT','UPDATE','DELETE','POST', 'OPTIONS'])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def increment_product_in_cart():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method == 'POST':         
                if request.data:
                    data = request.get_json()
                    unicode = int(data["product"])
                    user = int(data["user"])
                    cart=db.session.query(Panier).filter(Panier.client==user).first()
                    productToIncrement=None
                    for product in cart.produits['produits']:
                        if int(product['id'])==unicode:
                            productToIncrement=product
                    if productToIncrement:
                        #print(productToIncrement)
                        l=list(cart.produits['produits'])
                        #cart.taille=cart.taille+1
                        #cart.total=cart.total+(int(productToIncrement['prix'])/int(productToIncrement['index']))
                        cart.produits={"produits":[]}
                        cart.taille=0
                        cart.total=0
                        cart.totalReduit=0
                        db.session.add(cart)
                        db.session.commit()
                        
                        for product in l:
                            if int(product['id'])==int(productToIncrement['id']):
                                product['prix']=int(product['prix'])+(int(product['prix'])/int(product['index']))
                                product['prixReduit']=int(product['prixReduit'])+(int(product['prixReduit'])/int(product['index']))
                                product['index']=int(product['index'])+1
                        
                       
                       
                        for p in l:
                            cart.total=cart.total+int(p['prix'])
                            cart.totalReduit=cart.totalReduit+int(p['prixReduit'])
                            cart.taille=cart.taille+int(p['index'])
                            db.session.add(cart)
                            db.session.commit()
                        
                        cart.produits={"produits":l}
                        db.session.add(cart)
                        db.session.commit()

                        retour={"title":"Produit incrementé","contenu":"Produit incrementé dans le panier avec succes.","code":200}
                        return make_response(jsonify(retour),200)
                    
                    else:
                        retour={"title":"Produit non trouvé","contenu":"Produit non trouvé dans le panier.","code":404}
                        return make_response(jsonify(retour),404)
                    
                else:
                    retour={"title":"Données non trouvées","contenu":"Données non trouvées","code":500}
                    return make_response(jsonify(retour),500)
                    
          
    else:
        retour={"title":"Méthode Non Authorisée","contenu":"Cette interface n'accepte que la méthode POST.","code":405}
        return make_response(jsonify(retour),405)


@app.route('/cart/product/decrement', methods=['GET','POST','PUT','UPDATE','DELETE','POST', 'OPTIONS'])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def decrement_product_in_cart():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method == 'POST':         
                if request.data:
                    data = request.get_json()
                    unicode = int(data["product"])
                    user = int(data["user"])
                    cart=db.session.query(Panier).filter(Panier.client==user).first()
                    productToIncrement=None
                    for product in cart.produits['produits']:
                        if int(product['id'])==unicode:
                            productToIncrement=product
                    if productToIncrement:
                        #print(productToIncrement)
                        l=list(cart.produits['produits'])
                        #cart.taille=cart.taille-1
                        #cart.total=cart.total-(int(productToIncrement['prix'])/int(productToIncrement['index']))
                        cart.produits={"produits":[]}
                        cart.taille=0
                        cart.totalReduit=0
                        cart.total=0
                        db.session.add(cart)
                        db.session.commit()
                        
                        for product in l:
                            if int(product['id'])==int(productToIncrement['id']):
                                product['prix']=int(product['prix'])-(int(product['prix'])/int(product['index']))
                                product['prixReduit']=int(product['prixReduit'])-(int(product['prixReduit'])/int(product['index']))
                                product['index']=int(product['index'])-1

                        for p in l:
                            cart.total=cart.total+int(p['prix'])
                            cart.totalReduit=cart.totalReduit+int(p['prixReduit'])
                            cart.taille=cart.taille+int(p['index'])
                            db.session.add(cart)
                            db.session.commit()    


                        cart.produits={"produits":l}
                        db.session.add(cart)
                        db.session.commit()

                        retour={"title":"Produit decrementé","contenu":"Produit decrementé dans le panier avec succes.","code":200}
                        return make_response(jsonify(retour),200)
                    
                    else:
                        retour={"title":"Produit non trouvé","contenu":"Produit non trouvé dans le panier.","code":404}
                        return make_response(jsonify(retour),404)
                    
                else:
                    retour={"title":"Données non trouvées","contenu":"Données non trouvées","code":500}
                    return make_response(jsonify(retour),500)
                    
          
    else:
        retour={"title":"Méthode Non Authorisée","contenu":"Cette interface n'accepte que la méthode POST.","code":405}
        return make_response(jsonify(retour),405)        



@app.route('/cart/validation', methods=['GET','POST','PUT','UPDATE','DELETE','POST', 'OPTIONS'])
@cross_origin(origin='https://admin.relwende.com', supports_credentials=True, methods=['GET', 'POST', 'OPTIONS'], headers=['Authorization', 'Content-Type'])
@auth.login_required
def validation_cart():
    if request.method == 'OPTIONS':
        return make_response('', 200)
    if request.method == 'POST':         
                if request.data:
                    data = request.get_json()
                    #unicode = int(data["product"])
                    user = int(data["user"])
                    cart=db.session.query(Panier).filter(Panier.client==user).first()
                    
                    date=data['date']
                    heure=data['heure']
                    addresseLivraison=data['addresseLivraison']
                    libele=data['libele']
                    dateEvenement=data['dateEvenement']
                    dureeLocation=int(data['dureeLocation'])
                    dateLivraisonSouhaite=data['dateLivraison']

                    produits1=cart.produits['produits']
                    quantite=cart.taille
                    dateLivraison=""                  
                    heureLivraison=""              
                    statut="En cours"
                    prod=[]
                    produits={}

                    total=cart.total
                    totalReduit=cart.totalReduit
                    for i in range(0,len(produits1)):
                        us=db.session.query(Categorie).filter(Categorie.id==produits1[i]["categorie"]).first()
                        produits1[i]["libeleCategorie"]=us.libele

                        prod.append(produits1[i])
                        #total+=produits1[i]["prix"]

                    produits["produits"]=prod   
                    produits["total"]=total
                    produits["totalReduit"]=totalReduit
                    commande=Commande(dureeLocation,quantite,date,dateEvenement,dateLivraison,dateLivraisonSouhaite,heure,heureLivraison,addresseLivraison,libele,statut,produits,user)

                    
                    #commande=Commande(dureeLocation,quantite,date,dateEvenement,dateLivraison,heure,heureLivraison,addresseLivraison,libele,statut,produits,user,dateLivraisonSouhaite)
                    db.session.add(commande)
                    db.session.commit()
                   
                    cart.taille=0
                    cart.total=0
                    cart.totalReduit=0
                    cart.produits={"produits":[]}
                    cart.statut="Pas de produits"
                    db.session.add(cart)
                    db.session.commit()

                    us=db.session.query(Client).filter(Client.id==user).first()
                    destinataire ="relwendestore@gmail.com"
       
                    expediteur= "contact@relwende.com"
                    sujet = "Reception d'une nouvelle commande"
                    message = MIMEMultipart()
                    message['From'] = expediteur
                    message['To'] = destinataire
                    message['Subject'] = sujet
                    corps_du_message = "Votre plateforme vient d'enregistrer une nouvelle commande de "+us.nom+" "+us.prenom+", rendez-vous sur https://admin.relwende.com pour plus de details"
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


                    retour={"title":"Creation de commande","contenu":"Commande crée avec succes.","code":200}
                    return make_response(jsonify(retour),200)
                    
                   
                else:
                    retour={"title":"Données non trouvées","contenu":"Données non trouvées","code":500}
                    return make_response(jsonify(retour),500)
                    
          
    else:
        retour={"title":"Méthode Non Authorisée","contenu":"Cette interface n'accepte que la méthode POST.","code":405}
        return make_response(jsonify(retour),405)        
