import random
from flask import Flask, render_template, session, redirect

def crear_tablero():
    return [" " for i in range(9)]

def casillas_disponibles(tablero):
    return [f"{k}" for k,v in enumerate(tablero) if v == " "]

def juego_terminado(tablero):
    casos = [[0,1,2], [3,4,5], [6,7,8],
             [0,3,6], [1,4,7], [2,5,8],
             [0,4,8], [2,4,6]]
    for i in casos:
        if tablero[i[0]] != " " and tablero[i[0]] == tablero[i[1]] == tablero[i[2]]:
            return [True, tablero[i[0]]]
    if not casillas_disponibles(tablero):
        return [True, None]
    return [False, None]
        

app = Flask(__name__)
app.secret_key = "Esto no debería ir aquí."

@app.route("/")
def index():
    if "figura_jugador" not in session:
        return render_template("elegir_figura.html")
    return render_template("tablero.html", terminado = juego_terminado(session["tablero"]))

@app.route("/elegir_figura/<figura>")
def elegir_figura(figura):
    if figura in ["x", "o"]:
        session["tablero"] = crear_tablero()
        session["figura_jugador"] = figura
        session["figura_maquina"] = "o" if figura == "x" else "x"
    return redirect("/")

@app.route("/tirada/<casilla>")
def tirada(casilla):
    if "figura_jugador" in session and casilla in casillas_disponibles(session["tablero"]) and not juego_terminado(session["tablero"])[0]:
        tablero = session["tablero"].copy()
        tablero[int(casilla)] = session["figura_jugador"]
        if not juego_terminado(tablero)[0]:
            tablero[int(random.choice(casillas_disponibles(tablero)))] = session["figura_maquina"]
        session["tablero"] = tablero
    return redirect("/")

@app.route("/nuevo_juego")
def nuevo_juego():
    session.pop("figura_jugador", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)