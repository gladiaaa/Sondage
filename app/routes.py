from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import User, Scrutin
from flask_bcrypt import Bcrypt
from datetime import datetime
from bson.objectid import ObjectId

bcrypt = Bcrypt()
routes = Blueprint('routes', __name__)

# Page d'accueil
@routes.route('/')
def home():
    scrutins = Scrutin.get_all()
    return render_template('home.html', scrutins=scrutins)

# Page d'inscription
@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Vérification des mots de passe
        if password != confirm_password:
            flash('Les mots de passe ne correspondent pas.', 'error')
            return redirect(url_for('routes.register'))

        # Vérification si l'utilisateur existe déjà
        if User.get_by_email(email):
            flash('Email déjà utilisé.', 'error')
            return redirect(url_for('routes.register'))

        # Enregistrement de l'utilisateur
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        User.create(username, email, hashed_password)
        flash('Inscription réussie. Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('routes.login'))

    return render_template('register.html')

# Page de connexion
@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.get_by_email(email)
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            flash('Connexion réussie.', 'success')
            return redirect(url_for('routes.home'))
        else:
            flash('Identifiants incorrects.', 'error')
            return redirect(url_for('routes.login'))

    return render_template('login.html')

# Déconnexion
@routes.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('is_admin', None)
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

        # Validation des données
        if not question or not options or not start_date or not end_date:
            flash('Tous les champs doivent être remplis.', 'error')
            return redirect(url_for('routes.scrutins'))

        # Vérification des dates
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            if start_date_obj >= end_date_obj:
                flash('La date de début doit être antérieure à la date de fin.', 'error')
                return redirect(url_for('routes.scrutins'))
        except ValueError:
            flash('Format de date invalide.', 'error')
            return redirect(url_for('routes.scrutins'))

        # Création d'un nouveau scrutin
        Scrutin.create(question, options, start_date, end_date, session['user_id'])
        flash('Scrutin créé avec succès.', 'success')
        return redirect(url_for('routes.scrutins'))

    user_scrutins = [scrutin for scrutin in Scrutin.get_all() if scrutin['creator_id'] == session['user_id']]
    return render_template('scrutins.html', scrutins=user_scrutins)

# Détails d'un scrutin
@routes.route('/scrutins/<string:scrutin_id>')
def scrutin_details(scrutin_id):
    scrutin = Scrutin.get(scrutin_id)
    if not scrutin:
        flash("Le scrutin demandé n'existe pas.", "error")
        return redirect(url_for('routes.home'))

    has_voted = False  # Implémentez une logique réelle pour vérifier si l'utilisateur a voté
    return render_template('scrutins_details.html', scrutin=scrutin, has_voted=has_voted)

# Enregistrer un vote
@routes.route('/vote/<string:scrutin_id>', methods=['POST'])
def vote(scrutin_id):
    scrutin = Scrutin.get(scrutin_id)
    if not scrutin:
        flash("Le scrutin demandé n'existe pas.", "error")
        return redirect(url_for('routes.home'))

    option = request.form['option']
    # Ajoutez ici une logique pour enregistrer le vote dans la base de données
    flash("Votre vote a été enregistré avec succès.", "success")
    return redirect(url_for('routes.scrutin_details', scrutin_id=scrutin_id))

# Suppression d'un scrutin
@routes.route('/scrutins/delete/<string:scrutin_id>', methods=['POST'])
def delete_scrutin(scrutin_id):
    scrutin = Scrutin.get(scrutin_id)

    # Vérification des droits de suppression
    if scrutin['creator_id'] != session.get('user_id') and not session.get('is_admin'):
        flash('Vous n\'avez pas la permission de supprimer ce scrutin.', 'error')
        return redirect(url_for('routes.scrutins'))

    Scrutin.delete(scrutin_id)
    flash('Scrutin supprimé avec succès.', 'success')
    return redirect(url_for('routes.scrutins'))
