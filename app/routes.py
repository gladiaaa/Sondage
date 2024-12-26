from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import mongo
from flask_bcrypt import Bcrypt
from datetime import datetime
from bson.objectid import ObjectId

bcrypt = Bcrypt()
routes = Blueprint('routes', __name__)

# Page d'accueil
@routes.route('/')
def home():
    scrutins = list(mongo.db.scrutins.find())
    return render_template('home.html', scrutins=scrutins)

# Page d'inscription
@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'error')
            return redirect(url_for('routes.register'))

        existing_user = mongo.db.users.find_one({"$or": [{"email": email}, {"username": username}]})
        if existing_user:
            flash('Nom d\'utilisateur ou email déjà utilisé.', 'error')
            return redirect(url_for('routes.register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        mongo.db.users.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password,
            "is_admin": False
        })
        flash('Inscription réussie. Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('routes.login'))

    return render_template('register.html')

# Page de connexion
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = mongo.db.users.find_one({"email": email})
        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['is_admin'] = user.get('is_admin', False)
            flash('Connexion réussie.', 'success')
            return redirect(url_for('routes.home'))
        else:
            flash('Identifiants incorrects.', 'error')
            return redirect(url_for('routes.login'))

    return render_template('login.html')

# Déconnexion
@routes.route('/logout')
def logout():
    session.clear()
    flash('Déconnexion réussie.', 'success')
    return redirect(url_for('routes.home'))

# Page de gestion des scrutins
@routes.route('/scrutins', methods=['GET', 'POST'])
def scrutins():
    if 'user_id' not in session:
        flash('Vous devez être connecté pour accéder à cette page.', 'error')
        return redirect(url_for('routes.login'))

    if request.method == 'POST':
        question = request.form['question']
        options = request.form.getlist('options[]')
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        if not question or len(options) < 2 or not start_date or not end_date:
            flash('Tous les champs doivent être remplis avec au moins deux options.', 'error')
            return redirect(url_for('routes.scrutins'))

        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            if start_date_obj >= end_date_obj:
                flash('La date de début doit être antérieure à la date de fin.', 'error')
                return redirect(url_for('routes.scrutins'))
        except ValueError:
            flash('Format de date invalide.', 'error')
            return redirect(url_for('routes.scrutins'))

        mongo.db.scrutins.insert_one({
            "question": question,
            "options": options,
            "start_date": start_date,
            "end_date": end_date,
            "creator_id": session['user_id']
        })
        flash('Scrutin créé avec succès.', 'success')
        return redirect(url_for('routes.scrutins'))

    user_scrutins = list(mongo.db.scrutins.find({"creator_id": session['user_id']}))
    return render_template('scrutins.html', scrutins=user_scrutins)

# Détails d'un scrutin
@routes.route('/scrutins/<scrutin_id>')
def scrutin_details(scrutin_id):
    scrutin = mongo.db.scrutins.find_one({"_id": ObjectId(scrutin_id)})
    if not scrutin:
        flash('Scrutin introuvable.', 'error')
        return redirect(url_for('routes.home'))
    return render_template('scrutins_details.html', scrutin=scrutin)

# Suppression d'un scrutin
@routes.route('/scrutins/delete/<scrutin_id>', methods=['POST'])
def delete_scrutin(scrutin_id):
    scrutin = mongo.db.scrutins.find_one({"_id": ObjectId(scrutin_id)})

    if not scrutin or (scrutin['creator_id'] != session.get('user_id') and not session.get('is_admin')):
        flash('Vous n\'avez pas la permission de supprimer ce scrutin.', 'error')
        return redirect(url_for('routes.scrutins'))

    mongo.db.scrutins.delete_one({"_id": ObjectId(scrutin_id)})
    flash('Scrutin supprimé avec succès.', 'success')
    return redirect(url_for('routes.scrutins'))
