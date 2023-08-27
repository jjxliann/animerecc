from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required,current_user
from .models import Anime
from .import db
import json


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method =='POST':
        anime = request.form.get('anime')

        if len(anime) <1:
            flash('Please enter valid anime name', category='error')
        else:
            new_anime = Anime(data=anime,user_id=current_user.id)
            db.session.add(new_anime)
            db.session.commit()
            flash('Searchin')
    return render_template("home.html", user=current_user)

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

