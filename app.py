import os

import pdfkit as pdfkit
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, current_user, logout_user, UserMixin
from peewee import *
# import pdfkit
from werkzeug.utils import secure_filename


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

ALLOWED_EXTENSIONS = set(['txt', 'csv'])

#pour uploader les fichiers
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/index', methods=['POST','GET'])
def index():
    return render_template('index.html')


paths=[]
@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                paths.append(path)
        flash('File(s) successfully uploaded')

        #création des bases de données
        database.create_table_person(paths[0])
        database.create_table_post(paths[1])
        database.create_table_skill(paths[2])

        return redirect('/index')


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
                return redirect('/index')
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


@app.route('/upload', methods=['GET', 'POST'])
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
