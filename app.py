import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.utils import secure_filename

from model import database
from model.constants import *
import model.database
from plannificateur.main import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')
# Make directory if "uploads" folder not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'csv'}


# pour uploader les fichiers
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/create-firm-name')
def create_firm_name():
    if current_user.is_authenticated:
        user = database.User.get(username=current_user.username)
        user.firm_name = "My Firm"
        user.save()
        return "Firm name created"
    else:
        return "Not logged in"


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

    return render_template('upload.html')


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/index', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


# base de données pour les utilisateurs


@login_manager.user_loader
def load_user(user_id):
    return database.User.get(user_id)  # TODO: charger une instance de User à partir d'une ID user


@app.before_request
def before_request():
    database.db.connect()


@app.after_request
def after_request(response):
    database.db.close()
    return response


# the user model specifies its fields (or columns) declaratively


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # store the user in the database
        database.User.create(username=username, password=hashed_password)
        return redirect('/login')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = database.User.get(database.User.username == username)
            # check if the password is correct
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect('/upload')
            else:
                return 'Incorrect password'
        except database.User.DoesNotExist:
            return 'Incorrect username'
    return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this page."


@app.route('/uploadusername', methods=['GET', 'POST'])
@login_required
def upload_page():
    return f"L'utilisateur actuel est {current_user.username}"
    pass  # TODO


@app.route('/us')
def us():
    return render_template('us.html')


@app.route("/")
def launching():
    return render_template("launchingpage.html")

@app.route("/result", methods=["POST", "GET"])
def result():
    # création des bases de données
    file_name1 = "person.csv"
    file_path1 = os.path.join(app.config['UPLOAD_FOLDER'], file_name1)
    database.create_table_person(file_path1, current_user.username)
    file_name2 = "post.csv"
    file_path2 = os.path.join(app.config['UPLOAD_FOLDER'], file_name2)
    database.create_table_post(file_path2, current_user.username)
    file_name3 = "skill.csv"
    file_path3 = os.path.join(app.config['UPLOAD_FOLDER'], file_name3)
    database.create_table_skill(file_path3, current_user.username)
    colis = int(request.form['nb_colis'])
    pieces = int(request.form['nb_pieces'])
    # utilisation de la fonction RO de création de planning
    resultat = plannificateur.RO3.planning(current_user.username, colis, pieces)


    return render_template("result.html", days=DAYS, posts=POSTS2,
                           planning=resultat[0], nb_person=resultat[2], nb_interim=resultat[1])


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
