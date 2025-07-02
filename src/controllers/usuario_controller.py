from flask import render_template, request 
from flask_controller import FlaskController
from src.models.usuarios import usuario
from src.app import app


class usuariosController(FlaskController):
      
      
    @app.route('/formulario_usuario')
    def formulario_usuario():
        
        return render_template('formulario_usuario.html',titulo='iniciar sesion')
    

@app.route('/formulario_Nue_usuario',)
def formulario_Nue_usuario():
   
    return render_template('formulario_Nue_usuario.html',titulo='registrarse')


@app.route('/lista_usuarios')
def lista_usuarios():
    try:
        usuarios = usuario.traer_usuarios()

        return render_template('lista_usuarios.html',titulo='lista de usuarios',usuarios=usuarios)
    except: 
                return render_template('lista_usuarios.html',titulo='Error de conexión a la base de datos')
    