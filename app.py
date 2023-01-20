import os

import pdfkit as pdfkit
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, send_from_directory
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, current_user, logout_user, UserMixin
from peewee import *
# import pdfkit
from werkzeug.utils import secure_filename


import plannificateur.database

from plannificateur.constants import *
#from plannificateur.database import *
#from plannificateur.RO3 import *





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

#pour uploader les fichiers
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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


#création des bases de données


file_name1 = "person.csv"
file_path1 = os.path.abspath(file_name1)
plannificateur.database.create_table_person(file_path1)

file_name2 = "post.csv"
file_path2 = os.path.abspath(file_name2)
plannificateur.database.create_table_post(file_path2)


file_name3 = "skill.csv"
file_path3 = os.path.abspath(file_name3)
plannificateur.database.create_table_skill(file_path3)


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/index', methods=['POST','GET'])
def index():
    return render_template('index.html')




# base de données pour les utilisateurs
DATABASE = 'database2.db'
database = SqliteDatabase(DATABASE)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)  # TODO: charger une instance de User à partir d'une ID user


@app.before_request
def before_request():
    database.connect()


@app.after_request
def after_request(response):
    database.close()
    return response


class BaseModel(Model):
    class Meta:
        database = database


# the user model specifies its fields (or columns) declaratively, like django
class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


def create_tables():
    with database:
        database.create_tables([User])


create_tables()



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # store the user in the database
        User.create(username=username, password=hashed_password)
        return redirect('/index')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = User.get(User.username == username)
            # check if the password is correct
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect('/upload')
            else:
                return 'Incorrect password'
        except User.DoesNotExist:
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




@app.route("/result", methods=["POST"])
def result():
    colis=request.form['nb_colis']
    pieces=request.form['nb_pieces']
    #retour=RO3.main(current_user.username,colis, pieces)
    return render_template("result.html", days=DAYS, posts=POSTS,
                           planning=RETURN_EXAMPLE[0],nb_person=RETURN_EXAMPLE[1], nb_interim=RETURN_EXAMPLE[2])


# A voir l'utilité de cette fonction: on peut imprimer directement à l'aide du navigateur
@app.route("/pdf")
def convert_to_pdf():
    name = "planning"
    html = render_template(
        "result.html",
        name=name)
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
