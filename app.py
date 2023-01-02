from flask import Flask, render_template, request

app=Flask(__name__)




@app.route("/")

def index():
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def result():
    days = {"Lundi": 0, "Mardi": 0, "Mercredi": 0, "Jeudi": 0, "Vendredi": 0, "Samedi": 0}
    return render_template("result.html",
                           title="Résultats",
                           results=days)


if __name__ == '__main__':
    app.run(debug=True)

#difficultés
#afficher une image en arrière plan

