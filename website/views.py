
from flask import Blueprint, render_template, request, flash, jsonify, redirect,url_for, session
from flask_login import login_required,current_user
from .models import Anime
from .search import search
from .import db
from itertools import chain
import json


views = Blueprint('views', __name__)

global reccs


@views.route("/", methods=['GET', 'POST'])
@login_required
def home():
    global reccs
    reccs = session.get('reccs',None)
                                
    if request.method == 'POST':
         anime = request.form.get('anime')
         print(request.form.getlist('anime'))
         new_anime = Anime(data=anime,user_id=current_user.id)
         db.session.add(new_anime)
         db.session.commit()
    return render_template("home.html", reccs = reccs, user=current_user)
   

"""if request.method =='POST':
        request.form(anime)

        if len(anime) <1:
            flash('Please enter valid anime name', category='error')
        else:
          
           
           new_anime = Anime(data=anime,user_id=current_user.id)
            db.session.add(new_anime)
            db.session.commit()
            flash('Searchin') """""
    

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
        

        

      
 


@views.route('/delete-anime', methods=['POST'])
def delete_anime():
    anime = json.loads(request.data)
    animeId = anime['anime']
    anime = Anime.query.get(animeId)
    if anime:
        if anime.user_id == current_user.id:
            db.session.delete(anime)
            db.session.commit()
            return jsonify({})

