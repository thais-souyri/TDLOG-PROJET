from flask import Flask, render_template, request
from plannificateur.constants import *

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", entry=MONTHS)



@app.route("/result", methods=["POST"])
def result2():
    return render_template("result.html", days=DAYS, posts=POSTS,
                           planning=PLANNING_EXAMPLE)


if __name__ == '__main__':
    app.run(debug=True)

# difficultés
# afficher une image en arrière plan
