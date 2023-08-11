"""
API routes for users movies web app using Flask
Using
Users Blueprint
Movies Blueprint
"""
import os

from flask import Flask, render_template, g
from flask_cors import CORS

from movieflix_db.data_manager.data_models import User, Movie, db
from movieflix_db.data_manager.users import Users
from movieflix_db.data_manager.movies import Movies
from movieflix_db.data_manager.sqlite_data_manager import SQLiteDataManager
from users_routes import users_bp
from movies_routes import movies_bp

app = Flask(__name__)
app.app_context()

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data/movieflix.sqlite')

db.init_app(app)
with app.app_context():
    db.create_all()

users_data_manager = Users(SQLiteDataManager('id', User, db))
movies_data_manager = Movies(SQLiteDataManager('id', Movie, db))


app.register_blueprint(users_bp)
app.register_blueprint(movies_bp)

CORS(app)


@app.before_request
def before_request():
    g.users_data_manager = users_data_manager
    g.movies_data_manager = movies_data_manager


@app.route('/')
def home():
    """
    Home page
    :return:
        render index.html page.
    """
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(_error):
    """
    Handle 404, Not Found Error
    returns:
        Page Not Found page, 404
    """
    return render_template('404.html'), 404


@app.errorhandler(400)
def bad_request_error(error):
    """
    Handle 400, Bad Request Error
    returns:
        Bad request page, 400
    """
    print(error)
    return render_template('400.html', errors=error.description), 400


@app.errorhandler(500)
def internal_server_error(_error):
    """
    Handle 500, Internal Server Error
    returns:
        Internal Server page, 500
    """
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(port=5002)
