from models import *
from getpass import *
from collections import OrderedDict

def userpass():
	'''Please enter your new username and password below'''
	print '=============================================='
	try:
		user_id = input('Enter the User id: ')
		user = User.get(User.id==user_id)
	except User.DoesNotExist:
		print 'User does not exist in the database please create a new user'
	except:
		pass
	print '===================================================='
		
	username = raw_input('Username: ')
	pass1 = getpass('Password: ')
	if pass1 == '':
		pass
	pass2 = getpass('Comfirm Password: ')
	opt = raw_input('Do you want to continue [y,n]: ').lower().strip()
	if opt == 'y':
		if pass1 == pass2 and username:
			user.username=username 
			user.password=pass1
			user.save()
			print 'Data havw been saved'
		else:
			print 'Passwords do not march or username was blank'
	else:
		print 'Aborted'

	print'====================================================='

def new():
	'''Please enter your new details'''
	print '===================================================='
	username = raw_input('Username: ')
	if User.select().where(User.username == username):
		print 'Username already in use. please choose a different name.'
		print '======================================================'
		return
	pass1 = getpass('Password: ')
	if pass1 == '':
		pass
	pass2 = getpass('Confirm Password: ')
	opt = raw_input('Do you want to continue [y,n]: ').lower().strip()
	if opt == 'y':
		if pass1 == pass2 and username:
			User.create(username=username, password=pass1)
			print 'New user have been created successfully.'
		else:
			print "Passowrds didn't match or username was blank"
	else:
		print 'Aborted'
	print '====================================================='



def password():
	'''Please enter your new password below'''
	print '======================================================'
	try:
		user_id = input('Please Enter your user id: ')
		user = User.get(User.id == user_id)
		pass1 = getpass('Password: ')
		if pass1 == '':
			pass
		pass2 = getpass('Confirm Password: ')
		opt = raw_input('Do u want to continue [y,n]: ').lower().strip()
		if opt == 'y':
			if pass1 == pass2:
				user.password=pass1
				user.save()
				print 'Passowrd changed'
			else:
				print 'Passwords do not match'
		else:
			print 'Aborted'
	except User.DoesNotExist:
                print 'User does not exist'
             
	except:
		pass 
	print '==================================================='


def deleteUser():
	'''Delete an existing user by supplying his/her user id'''
	print '===================================================='
	try:
		user_id = input('Please enter the user id: ')
		user = User.get(User.id == user_id)
		opt = raw_input('Do you want to contine [y,n]: ').lower().strip()
		if opt == 'y':
			user.delete_instance()
			print 'User deleted'
		else:
			'Print Aborted'
	except:
		print 'User does not exist'
	print '====================================================='

def getusers():
	'Get all users with their ids'
	print '====================================================='
	for user in User.select():
		print `user.id`, user.username
	print '====================================================='

def main_loop():
	choice = None
	print 'Enter "quit" to exit'
	while choice != 'quit':
		for key, value in menu.items():
			print ('%s) %s' % (key, value.__doc__))
		choice = raw_input('Action: ').lower().strip()
		if choice in menu:
			menu[choice]()


menu = OrderedDict([
	('n',new),
	('u',userpass),
	('p', password),
	('g',getusers),
	('d', deleteUser),
])


if __name__=='__main__':
	main_loop()
