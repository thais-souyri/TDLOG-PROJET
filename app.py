import os

from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, current_user, logout_user, UserMixin
from peewee import *
# import pdfkit
from werkzeug.utils import secure_filename

from plannificateur.constants import *
from plannificateur.RO3 import *


ALLOWED_EXTENSIONS = {'csv', 'txt'}

login_manager = LoginManager()

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads/'

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


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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


@app.route('/file', methods=['GET', 'POST'])
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
            return redirect("launching")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            return redirect(url_for('index'))
    return render_template("launchingpage.html")


@app.route('/us')
def us():
    return render_template('us.html')


@app.route("/")
def launching():
    return render_template("launchingpage.html")


@app.route("/index", methods=['POST', 'GET'])
@login_required
def index():
    return render_template("index.html", entry=MONTHS)


@app.route("/result", methods=["POST"])
def result():
    return render_template("result.html", days=DAYS, posts=POSTS,
                           planning=PLANNING_EXAMPLE)


# A voir l'utilité de cette fonction: on peut imprimer directment à l'aide du navigateur
@app.route("/")
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
