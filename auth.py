from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask.views import MethodView
from flask_login import login_user, logout_user
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length
from playhouse.flask_utils import get_object_or_404
from models import User
from my_forms import LoginForm

auth = Blueprint('auth',__name__, template_folder='templates')


class LoginView(MethodView):
		


	def get(self):
		u = User.select().count()
		if u != 0:
			form = LoginForm()

			return render_template('auth/login.html', form=form)
		else:
			content = 'There are no users, please create a user'
			return render_template('info.html', content=content)

	def post(self):
		#context = self.get_context()

		form = LoginForm()
		
		if form.validate_on_submit():
			try:
				user = User.get(User.username==form.username.data)
				if user is not None and user.verify_password(form.password.data):
					login_user(user, form.remember_me.data)
					return redirect(request.args.get('next') or url_for('admin.index'))
			except User.DoesNotExist:
				pass
		return render_template('auth/login.html', form=form)	

class LogoutView(MethodView):
	
	def get(self):
		logout_user()
		return redirect('/')

# Register the urls
auth.add_url_rule('/login/', view_func=LoginView.as_view('login'))
auth.add_url_rule('/logout/', view_func=LogoutView.as_view('logout'))
