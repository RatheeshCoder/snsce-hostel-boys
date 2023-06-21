from flask import Flask, Blueprint

def create():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "abc123"
    from .views import views
    app.register_blueprint(views, url_prefix='/')
    return app
