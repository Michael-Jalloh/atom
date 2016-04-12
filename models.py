from peewee import *
import re
import datetime
from hashlib import md5
from flask import Markup
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from playhouse.sqlite_ext import *
from atom import flask_db, database, login_manager, SITE_WIDTH
from config import POST_PER_PAGE as ppp



class User(UserMixin, flask_db.Model):
	email = CharField(unique=True, default='')
	username = CharField()
	password_hash = CharField()
	admin = BooleanField(default=False)
	about_me = TextField(default='')
	

	def avatar(self, size):
				return 'https://secure.gravatar.com/avatar/%s?d=identicon&s=%d' %( md5(self.email.encode('utf-8')).hexdigest(), size)

	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')



	@property
	def html_content(self):
                
	# This function will be use to turn our post content into html
		hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
		extras = ExtraExtension()
		content = self.converter()
		markdown_content = markdown(content, extensions=[hilite, extras])
		#       oembed_content = parse_html(
		#               markdown_content,
				#       oembed_providers,
		#               urlize_all=True,
		#               maxwidth=SITE_WIDTH)

		return Markup(markdown_content)


	def converter(self):
                conv = ''
		content = self.about_me
		while 1:
        		try:
                        	if '<pre>' in content:
                                        first, rest = content.split('<pre>',1)
					code, content = rest.split('</pre>',1)
					conv = conv+first.replace('\n','<br>')+'<pre>'+code+'</pre>'
				else:
					conv = conv + content.replace('\n','<br>')
					break
			except:
				break
		return conv


	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)
	
	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	
	@login_manager.user_loader
	def load_user(user_id):
		return User.get(User.id == int(user_id))

class Post(flask_db.Model):
	title = CharField()
	slug = CharField(unique=True)
	published = BooleanField(default=False,index=True)
	timestamp = DateTimeField(default=datetime.datetime.utcnow, index=True)
	content = TextField()
	author = ForeignKeyField(User, related_name='posts')
	link = CharField(default='')

        @property
	def link_code(self):
                return Markup(self.link)
	
	def save(self, *args, **kwargs):
		self.slug = re.sub('[^\w]+', '-', self.title.lower())
		ret = super(Post, self).save(*args, **kwargs)

		# Store search content
		self.update_search_index()
		return ret

	def update_search_index(self):
		PostIndex.delete().where(PostIndex.post_id == self.id).execute()
		index = PostIndex(post_id = self.id, published=self.published)
		index.content = '\n'.join((self.title,self.content))
		index.save()

	def converter(self):
		conv = ''
		content = self.content
		while 1:
			try:
				if '<pre>' in content:
					first, rest = content.split('<pre>',1)
					code, content = rest.split('</pre>',1)
					conv = conv+first.replace('\n','<br>')+'<pre>'+code+'</pre>'
				else:
					conv = conv + content.replace('\n','<br>')
					break
			except:
				break
		return conv

	@classmethod
	def max_post_page_all(self):
		m = float(Post.select().count())/ ppp
		n = Post.select().count()/ ppp
		if m>n:
			n = n +1
		return n
		
	@classmethod
	def max_post_page_public(self):
		m = float(Post.public().count())/ ppp
		n = Post.public().count() / ppp
		if m>n:
			n = n + 1
		return n
		

	@property
	def html_content(self):
	# This function will be use to turn our post content into html
		hilite = CodeHiliteExtension(linenums=False, css_class='highlight')
		extras = ExtraExtension()
		content = self.converter()
		markdown_content = markdown(content, extensions=[hilite, extras])
	#	oembed_content = parse_html(
	#		markdown_content,
		#	oembed_providers,
	#		urlize_all=True,
	#		maxwidth=SITE_WIDTH)

		return Markup(markdown_content)





	@classmethod
	def public(cls):
		return Post.select().where(Post.published == True)


	
	@classmethod
	def private(cls):
		return Post.select().where(Post.published == False)


	@classmethod
	def search(cls, query):
		words = [word.strip() for word in query.split() if word.strip()]
		if not words:
			# Return empty query.
			return Post.public().where(Post.id == 0)
		else:
			ids = []
			posts = []
			for word in words:
				indexes = PostIndex.search(word)
				for post_search in indexes:
					if post_search.post_id in ids or post_search.post_id == None:
						pass
					else:
						ids.append(post_search.post_id)
						post = Post.get(id=post_search.post_id)
						if post.published == True:
							posts.append(post)
	
		return posts

	@classmethod
	def search_all(cls, query):
		words = [word.strip() for word in query.split() if word.split()]
		if not words:
			# Return and empty query
			return Post.select().where(Post.id == 0)
		else:
			ids = []
			post = []
			for word in words:
				indexes = PostIndex.search(word)
				for post_search in indexes:
					if post_search.post_id in ids or post_search.post_id == None:
						pass
					else:
						ids.append(post_search.post_id)
						post = Post.get(id=post_search.post_id)
						posts.append(post)
		return posts

class PostIndex(FTSModel):
	post_id = IntegerField()
	content = TextField()
	published = BooleanField()



	@classmethod
	def max_post_page_all(cls,query):
		m = float(PostIndex.search(query).count()) / ppp
		n = PostIndex.search(query).count() / ppp
		if m > n:
			n = n + 1
		return n

	@classmethod
	def max_post_page_public(cls, query):
		m = float(PostIndex.search(query).where(PostIndex.published==True).count()) / ppp
		n = PostIndex.search(query).where(PostIndex.published==True).count() / ppp
		if m > n:
			n = n + 1
		return n

	

	class Meta:
		database = database


class Comment(flask_db.Model):
	timestamp = DateTimeField(default=datetime.datetime.utcnow, index=True)
	content = TextField()
	author = CharField()
	post = ForeignKeyField(Post, related_name='comments')	
	email = CharField(default='')

	def avatar(self, size):
		return 'https://secure.gravatar.com/avatar/%s?d=identicon&s=%d' %( md5(self.email.encode('utf-8')).hexdigest(), size)


database.create_tables([ User, Post, PostIndex, Comment], safe=True)
