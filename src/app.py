from flask import Flask
from flask_controller import FlaskControllerRegister
from src.models import Base, engine
from src.controllers.acciones_controller import acciones_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret key'


register_controllers = FlaskControllerRegister(app)
register_controllers.register_package('src.controllers')

app.register_blueprint(acciones_bp)

Base.metadata.create_all(engine)  

if __name__ == '__main__':
    app.run(debug=True)
 

