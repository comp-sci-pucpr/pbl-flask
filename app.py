from flask import Flask, render_template, request, redirect, url_for, flash
import json
from usuarios import usuarios_blueprint

app = Flask(__name__)
app.register_blueprint(usuarios_blueprint)
app.config['SECRET_KEY'] = "chave_secreta"
privilegio = ''


@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login_form", methods = ["GET", "POST"])
def login_form():
    if request.method=="POST":
        global privilegio
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        with open("usuarios.json", "r") as arquivo_leitura:
            usuarios:dict = json.load(arquivo_leitura)

        if usuario in usuarios.keys() and usuarios[usuario]["senha"] == senha:
            if usuarios[usuario]["privilegio"] == "admin":
                privilegio="admin"
            return redirect("home")

        flash("Login Invalido")
    return redirect("/")

@app.route("/home")
def home():
    if privilegio =="admin":
        return redirect("adm")
    return redirect("usuario")

@app.route("/adm")
def adm():
    return render_template("adm.html")

@app.route("/usuario")
def usuario():
    return render_template("usuario.html")

@app.route("/sair")
def sair():
    global privilegio
    privilegio=""
    return redirect("/")

if __name__ == "__main__":
    app.run("0.0.0.0", port=80, debug=True)