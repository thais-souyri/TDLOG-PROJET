# importations

import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.utils import secure_filename

from model import database
import model.database
from plannificateur.main import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Création du fichier pour uploader les fichiers csv

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')
# Make directory if "uploads" folder not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# types de fichiers autorisés
ALLOWED_EXTENSIONS = {'csv'}


# fonctions permettant de gérer l'authentification

# charge une instance de User à partir d'une ID user
@login_manager.user_loader
def load_user(user_id):
    return model.database.User.get(user_id)


@app.before_request
def before_request():
    model.database.db.connect()


@app.after_request
def after_request(response):
    model.database.db.close()
    return response


@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this page."


# crée le firm name à partir du nom d'utilisateur si l'utilisateur est connecté
@app.route('/create-firm-name')
def create_firm_name():
    if current_user.is_authenticated:
        user = model.database.User.get(username=current_user.username)
        user.firm_name = "My Firm"
        user.save()
        return "Firm name created"
    else:
        return "Not logged in"


# permet de rediriger vers la page de lancement
@app.route("/")
def launching():
    return render_template("launchingpage.html")


# vérifie si un fichier est au format csv
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# permet à l'utilisateur d'uploader ses fichiers csv dans le dossier prévu
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))

    return render_template('first_login.html')


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


# crée le nom d'utilisateur et le mot de passe
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # hashe le mot de passe
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # stocke l'utilisateur dans la base de données
        model.database.User.create(username=username, password=hashed_password)
        return redirect('/first')
    return render_template('register.html')


# on upload les fichiers à la première connexion
@app.route('/first', methods=['GET', 'POST'])
def first_login():
    return redirect('/upload')


@app.route('/to_login', methods=['GET', 'POST'])
def to_login():
    return render_template('login1.html')


# la base de données est créée uniquement à la première connexion, à partir du nom d'utilisateur

@app.route('/login1', methods=['GET', 'POST'])
def login1():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = model.database.User.get(model.database.User.username == username)

            # check if the password is correct
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                # création des bases de données
                file_name1 = "person.csv"
                file_path1 = os.path.join(app.config['UPLOAD_FOLDER'], file_name1)
                model.database.create_table_person(file_path1, current_user.username)
                file_name2 = "post.csv"
                file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], file_name2)
                model.database.create_table_post(file_path2, current_user.username)
                file_name3 = "skill.csv"
                file_path3 = os.path.join(app.config['UPLOAD_FOLDER'], file_name3)
                model.database.create_table_skill(file_path3, current_user.username)

                return render_template('package.html')
            else:
                return 'Incorrect password'
        except model.database.User.DoesNotExist:
            return 'Incorrect username'

    return render_template('first_login.html')


# permet à l'utilisateur de se connecter (même fonction que la précédente à l'exception qu'elle ne crée pas la base de données)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = model.database.User.get(model.database.User.username == username)

            # check if the password is correct
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return render_template('package.html')
            else:
                return render_template('incorrect_password.html')
        except model.database.User.DoesNotExist:
            return render_template('incorrect_username.html')

    return render_template('login.html')




# permet de se déconnecter
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


# permet de rediriger vers la page à propos de nous
@app.route('/us')
def us():
    return render_template('us.html')


# utilise les infos de l'utilisateur et redirige vers la page de planning
@app.route("/result", methods=["POST", "GET"])
def result():
    # on récupère le nombre de colis à traiter et le nombre de pièces par colis, renseignés par l'utilisateur
    colis = int(request.form['nb_colis'])
    pieces = int(request.form['nb_pieces'])
    # utilisation de la fonction RO de création de planning
    resultat = plannificateur.main.main(current_user.username, colis, pieces)

    return render_template("result.html", days=DAYS, posts=POSTS2,
                           planning=resultat[0], nb_person=resultat[2], nb_interim=resultat[1])


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
