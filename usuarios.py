from flask import Flask, render_template, redirect, Blueprint, request, flash
import json
usuarios_blueprint = Blueprint("usuarios", __name__)

@usuarios_blueprint.route("/cadastrar_usuario")
def cadastrar_usuario():
    return render_template("cadastrar_usuario.html")

@usuarios_blueprint.route("/cadastrar_usuario_form", methods=["GET", "POST"])
def cadastrar_usuario_form():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")
        confirmar_senha = request.form.get("confirmar_senha")
        if senha != confirmar_senha:
            flash("As senhas devem ser iguais")
            return redirect("cadastrar_usuario")
        
        with open("usuarios.json", "r") as arquivo_leitura:
            usuarios:dict = json.load(arquivo_leitura)
        if usuario in usuarios.keys():
            flash("Usuario ja existente")
            return redirect("cadastrar_usuario")
        usuarios[usuario] = {}
        usuarios[usuario]["senha"] = senha
        usuarios[usuario]["privilegio"] = "usuario"
        with open("usuarios.json", "w") as arquivo_escrita:
            json.dump(usuarios, arquivo_escrita, indent=4)

        return redirect("home")
    flash("Metodo invalido de requisicao")    
    return redirect("cadastrar_usuario")