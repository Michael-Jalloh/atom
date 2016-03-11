from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo


class LoginForm(Form):
	username = StringField('Username', validators=[Required(), Length(1, 64)])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Keep me logged in')

class NewPasswordForm(Form):
	password1 = PasswordField('Password', validators=[Required(),EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	submit = SubmitField('Save')

class SignupForm(Form):
	email = StringField('Email', validators=[Required(), Length(1,64),
			Email()])
	username = StringField('Username', validators=[Required(), Length(1,64),			Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,
				'Username must have only letters, numbers, dots or underscores')])
	password1 = PasswordField('Password', validators=[Required(), EqualTo('password2', message='Passwords nust match.')])
	password2 = PasswordField('Confirm password', validators=[Required()])


	def validate_email(self,field):
		if User.select().where(User.email == field.data):
			raise ValidatorError('Email already registered.')
		
	def validate_username(self, field):
		if User.select().where(User.username == field.data):
			raise ValidatorError('Username already in use.')
