from flask_controller import FlaskController
from flask import render_template
from src.app import app


class homeController(FlaskController):

    @app.route('/')
    def    index():
        return render_template('index.html',titulo='inicio')
