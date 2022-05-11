from flask import Flask, redirect, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("busqueda.html")

@app.route("/pokemon", methods=["POST"])
def pokemon():
    nombre = request.form.get("nombre", None)
    page = requests.get(f"https://pokeapi.co/api/v2/pokemon/{nombre}")
    if page.status_code == 200:
        contenido = page.json()
        return render_template("pokemon.html",
                               nombre = nombre,
                               id = contenido["id"],
                               exp = contenido["base_experience"],
                               height = contenido["height"],
                               weight = contenido["weight"],
                               abilities = [i["ability"]["name"] for i in contenido["abilities"]],
                               imagen = contenido["sprites"]["front_default"])
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)