from flask import Flask
from flask.ext.login import LoginManager
from playhouse.flask_utils import FlaskDB


SITE_WIDTH = 800
application = Flask(__name__)
application.config.from_object('config')

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view ='auth.login'

flask_db = FlaskDB(application)
database = flask_db.database

def register_blueprints(app):
	# Prevents circular imports
	from views import posts
	from admin import admin
	from auth import auth
	from profile import profile
	application.register_blueprint(posts)
	application.register_blueprint(admin)
	application.register_blueprint(auth)
	application.register_blueprint(profile)
	login_manager.init_app(app)


register_blueprints(application)

if __name__ == '__main__':
	application.run()
