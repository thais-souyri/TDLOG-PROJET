from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
import pdfkit
from werkzeug.utils import secure_filename
from plannificateur.constants import *
import os

from plannificateur.tabledef import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import *
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

UPLOAD_FOLDER = '/Users/adeli/OneDrive'
ALLOWED_EXTENSIONS = {'csv', 'txt'}

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/adeli/OneDrive/Bureau/Ponts2A/TDLOG/Projet/TDLOG-PROJET/database2.db'
app.config['SECRET_KEY'] = 'secret_key'


class User2(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")



app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
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
            return path
    return render_template("launchingpage.html")


@app.route('/us')
def us():
    return render_template('us.html')


@app.route("/")
def launching():
    return render_template("launchingpage.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/index")
def index():
    return render_template("index.html", entry=MONTHS)


# routeur "fantôme" pour pouvoir utiliser les méthodes POST et GET pour index
@app.route("/setvolumetry", methods=["POST"])
def vol():
    return redirect(url_for("index"))


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
