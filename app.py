from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
import pdfkit
from werkzeug.utils import secure_filename
from plannificateur.constants import *
import os
from sqlalchemy.orm import sessionmaker
from plannificateur.tabledef import *
engine = create_engine('sqlite:///tutorial.db', echo=True)

UPLOAD_FOLDER = '/Users/adeli/OneDrive'
ALLOWED_EXTENSIONS = {'csv', 'txt'}

app = Flask(__name__)
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

@app.route('/')
def home():
    #if not session.get('logged_in'):
        #return render_template('launchingpage.html')
    #else:
        return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def do_admin_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()



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


#A voir l'utilité de cette fonction: on peut imprimer directment à l'aide du navigateur
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