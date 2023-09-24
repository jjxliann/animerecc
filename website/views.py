
from flask import Blueprint, render_template, request, flash, jsonify, redirect,url_for, session
from flask_login import login_required,current_user
from .models import Anime
from .search import search
from .import db
from jikanpy import Jikan
import json
#from .randomFunctions import animeImage, randomAnime,   animeSynopsis


views = Blueprint('views', __name__)

jikan = Jikan()

global reccs


@views.route("/", methods=['GET', 'POST'])
@login_required
def home():
    global reccs
    reccs = session.get('reccs',None)


        
    if request.method == 'POST':
        
         anime = request.form.get('anime')
         print(request.form.getlist('anime'))
         for anime in anime:
            if anime == None:
                continue
            new_anime = Anime(data=anime,user_id=current_user.id)
            db.session.add(new_anime)
         db.session.commit()
    return render_template("home.html", reccs = reccs, user=current_user)
   

    

@views.route("/serch", methods=['GET','POST'])
def serch():
        if request.method =='POST':
            anime = request.form.get('anime')
            anime = anime.lower()
            global reccs
            reccs = search(anime)
            #reccs = reccs.to_dict()
            session['reccs'] = reccs
            return redirect(url_for('views.home'))
        else:
             return render_template("serch.html", user = current_user)

@views.route("/list",methods =['GET','POST'])
def watchlist():
     return render_template("list.html", user =current_user)


@views.route("/random", methods =['GET', 'POST'])
def random():
    global anime
    anime  = jikan.random(type='anime')
    
    def randomAnime():
        names = anime["data"]["titles"]
        names = names[0]["title"]
        return(names)
    
    def animeImage():
        img = anime["data"]["images"]["jpg"]["large_image_url"]
        return(img)
    
    def animeSynopsis():
        synopsis = anime["data"]["synopsis"]
        return(synopsis)
    
    if request.method=="POST" and request.form.get('animeRecc') != None:
        animeName = request.form.get('animeRecc')
        new_anime = Anime(data=animeName,user_id=current_user.id)
        db.session.add(new_anime)
        db.session.commit()
        return render_template("random.html", animeName = randomAnime(), image = animeImage(), synopsis = animeSynopsis(), user = current_user)

    
    return render_template("random.html", animeName = randomAnime(), image = animeImage(), synopsis = animeSynopsis(), user = current_user)
    

    

    
    
    
    
    
    """ if request.method =='GET':
        animeName = randomAnime(),
        image = animeImage(),
        synopsis = animeSynopsis()
        return render_template("random.html" , 
        animeName = animeName,
        image = image,
        synopsis = synopsis, 
        user = current_user)
     return("random.html")"""
    


        

        

      
 


@views.route('/delete-anime', methods=['POST'])
def delete_anime():
    anime = json.loads(request.data)
    animeId = anime['animeId']
    anime = Anime.query.get(animeId)
    if anime:
        if anime.user_id == current_user.id:
            db.session.delete(anime)
            db.session.commit()
    return jsonify({})

