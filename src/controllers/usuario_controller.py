from flask import render_template, request, session as flask_session
from src.models import session as db_session
from flask_controller import FlaskController
from src.models.usuarios import usuario
from src.app import app



class usuariosController(FlaskController):
      
      
    @app.route('/formulario_usuario')
    def formulario_usuario():
        
        return render_template('formulario_usuario.html',titulo='iniciar sesion')
    

@app.route('/formulario_Nue_usuario',methods=['GET','POST'])

def formulario_Nue_usuario():


    if request.method == 'POST':
            correo = request.form.get('correo')
            correo_repetido= usuario.traer_usuarios_correo(correo)

            nombre_persona = request.form.get('nombre_persona')       
            nombre_usuario  = request.form.get('nombre_usuario')
            usuario_repetido= usuario.traer_usuarios_usuario(nombre_usuario)
            contraseña = request.form.get('contraseña')
            tipo_usuario = request.form.get('tipo_usuario')
            usuario_almacenar = usuario(correo,nombre_persona,nombre_usuario,contraseña, tipo_usuario)

            if usuario_repetido:
                return render_template('formulario_usuario.html',titulo='error: nombre de usuario repetido',
                                        errorusuario ="nombre de usuario en uso"
                                    ,producto_almacenar=usuario_almacenar)
           
            if correo_repetido:
                return render_template('formulario_Nue_usuario.html',titulo='error correo repetido',
                                   errorcorreo="el correo no se puede repetir"
                                   ,usuario_almacenar=usuario_almacenar)

            try:
                usuario.crear_usuario(usuario_almacenar) 
        
        
            except Exception as e:
                db_session.rollback()
                print(f"Error al registrar el usuario: {e}")
                
                return render_template('formulario_Nue_usuario.html',titulo='error al registrar en la base de datos')        
    return render_template('formulario_Nue_usuario.html',titulo='registro de productos')

@app.route('/lista_usuarios')
def lista_usuarios():
    try:
        usuarios = usuario.traer_usuarios()

        return render_template('lista_usuarios.html',titulo='lista de usuarios',usuarios=usuarios)
    except: 
                return render_template('lista_usuarios.html',titulo='Error de conexión a la base de datos')
    