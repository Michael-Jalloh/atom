from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from flask_login import login_required, current_user
from wtfpeewee.orm import model_form
from models import User

profile = Blueprint('profile', __name__, template_folder='templates')

class ProfileView(MethodView):

	def get(self):
		if User.select().count() != 0:
			user = User.get(User.id == 1)
			return render_template('profile/user.html',user=user)
		else:
			content = 'There are no users, please create a user'
			return render_template('info.html', content=content)



class InfoView(MethodView):
	decorators = [login_required]


	def get_context(self):
		form_cls = model_form(User, exclude=('password_hash'))
		
		if request.method == 'POST':
			form = form_cls(request.form)
		else:
			form = form_cls(obj=current_user)
		return form


	def get(self):
		form = self.get_context()
		return render_template('profile/detail.html', form=form)

	
	def post(self):
		form = self.get_context()
		
		if form.validate():
			form.populate_obj(current_user)
			current_user.save()
			
			return render_template('profile/user.html',user=current_user)
		return render_template('profile/detail.html')

# Register the urls
profile.add_url_rule('/profile/info', view_func=InfoView.as_view('info'))
profile.add_url_rule('/profile/', view_func=ProfileView.as_view('profile'))
