from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from plannificateur.constants import *
import os
from flask import send_from_directory

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
            path=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            return redirect(url_for('index'))
            return path
    return render_template("launchingpage.html")


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route("/")
def launching():
    return render_template("launchingpage.html")


@app.route("/index")
def index():
    return render_template("index.html", entry=MONTHS)


#routeur "fantôme" pour pouvoir utiliser les méthodes POST et GET pour index
@app.route("/setvolumetry", methods=["POST"])
def vol():
    return redirect(url_for("index"))


@app.route("/result", methods=["POST"])
def result():
    return render_template("result.html", days=DAYS, posts=POSTS,
                           planning=PLANNING_EXAMPLE)


if __name__ == '__main__':
    app.run(debug=True)
