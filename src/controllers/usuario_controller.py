from flask import render_template, request, redirect, url_for,flash, session as flask_session
from src.models import session as db_session
from flask_controller import FlaskController
from src.models.usuarios import usuario
from src.app import app
from werkzeug.security import generate_password_hash,check_password_hash


class usuariosController(FlaskController):
      
      
    @app.route('/formulario_usuario', methods=['GET', 'POST'])
    def formulario_usuario():
        if request.method == 'POST':
            nombre = (request.form.get('user') or request.form.get('nombre_usuario') or '').strip()
            password = (request.form.get('password') or request.form.get('contraseña') or '').strip()
            print("DEBUG form:", request.form.to_dict())
            print("DEBUG parsed password (len):", len(password), " repr:", repr(password))

    
            
            if not nombre or not password:
                flash('Usuario y contraseña son obligatorios', 'danger')
                return render_template('formulario_usuario.html', titulo='iniciar sesion')
            user_obj = usuario.traer_usuarios_usuario(nombre)
            #busca al usuario
            if not  user_obj:
                flash('usuario no encontrado', 'danger')
                return render_template('formulario_usuario.html', titulo='iniciar sesion')
            #verifica la contraseña con la libreria de security
            if not check_password_hash(user_obj.contraseña, password):
                flash('contraseña incorrecta', 'danger')
                return render_template('formulario_usuario.html', titulo='iniciar sesion')

            # guarda solo lo que es necesario como el usuario el nombre y el correo
            flask_session['user_id'] = user_obj.id_usuario
            flask_session['user_name'] = user_obj.nombre_usuario
            flask_session['user_email'] = user_obj.correo
            
            flash(f'¡Bienvenido, {user_obj.nombre_usuario}', 'success')
            return redirect(url_for('lista_productos'))  

     
        return render_template('formulario_usuario.html', titulo='iniciar sesion')
    

@app.route('/logout')
def logout():
    flask_session.clear()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('formulario_usuario'))
    

@app.route('/formulario_Nue_usuario',methods=['GET','POST'])

def formulario_Nue_usuario():


    if request.method == 'POST':
        correo = (request.form.get('correo') or '').strip()
        correo_repetido = usuario.traer_usuarios_correo(correo)
        nombre_persona = (request.form.get('nombre_persona') or '').strip()
        nombre_usuario = (request.form.get('nombre_usuario') or '').strip()
        usuario_repetido = usuario.traer_usuarios_usuario(nombre_usuario)
        contraseña_raw = (request.form.get('contraseña') or '').strip()
        tipo_usuario = (request.form.get('tipo_usuario') or 'user').strip()

        form_data ={
            'correo': correo,
            'nombre_persona': nombre_persona,
            'nombre_usuario': nombre_usuario,
            'tipo_usuario': tipo_usuario
        }

        if not correo or not nombre_persona or not nombre_usuario or not contraseña_raw:
              flash('todos los campos son obligatorios', 'danger')
              return render_template('formulario_Nue_usuario.html', tiutlo='registro de usuario', form_data=form_data)
        

        if usuario_repetido:
            flash('Nombre de usuario en uso', 'danger')
            return render_template('formulario_Nue_usuario.html', titulo='Registro de usuario', form_data=form_data)

        if correo_repetido:
            flash('Correo ya registrado', 'danger')
            return render_template('formulario_Nue_usuario.html', titulo='Registro de usuario', form_data=form_data)
        
        contraseña_hash = generate_password_hash(contraseña_raw)

        nuevo_usuario= usuario(correo,nombre_persona, nombre_usuario,contraseña_hash,tipo_usuario)
        try:
            usuario.crear_usuario(nuevo_usuario)
            flash('usuario registrado correctamente. ya puedes iniciar session.', 'success')
            return redirect(url_for('formulario_usuario'))
        except Exception as e:
            db_session.rollback()
            flash(f'Error al registrar el usuario: {str(e)}', 'danger')
            return render_template('formulario_Nue_usuario.html', titulo='Registro de usuario', form_data=form_data)


    return render_template('formulario_Nue_usuario.html',titulo='registro de productos')




@app.route('/lista_usuarios')
def lista_usuarios():
    try:
        usuarios = usuario.traer_usuarios()
        return render_template('lista_usuarios.html',titulo='lista de usuarios',usuarios=usuarios)
    
    except Exception as e:
         
        flash('error en la coneccion de la base de datos', 'danger')
        return render_template('lista_usuarios.html',titulo='Error de conexión a la base de datos')
    