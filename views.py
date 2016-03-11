from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from playhouse.flask_utils import get_object_or_404
from models import Post, Comment, PostIndex
from wtfpeewee.orm import model_form
from flask.ext.login import login_required
from config import POST_PER_PAGE


posts = Blueprint('posts',__name__, template_folder='templates')


class ListView(MethodView):

	def get(self,page=1):
		search_query = request.args.get('q')
		if search_query:
			posts = Post.search(search_query)
			max_page = PostIndex.max_post_page_all(search_query)
		else:
			max_page = Post.max_post_page_all()
			posts = Post.select().order_by(Post.timestamp.desc()).paginate(page,POST_PER_PAGE)
		return render_template('posts/list.html', posts=posts, page=page, max_page= max_page)


class DetailView(MethodView):
	form =	model_form(Comment, exclude=['timestamp','post'])

	def get_context(self, slug):
		query = Post.select()
		post = get_object_or_404(query, Post.slug==slug)
		form = self.form(request.form)

		context = {
			'post': post,
			'form': form
		}

		return context

	
	def get(self, slug):
		context = self.get_context(slug)
		return render_template('posts/detail.html', **context)

	def post(self, slug):
		context = self.get_context(slug)
		form = context.get('form')

		if form.validate():
			comment = Comment()
			form.populate_obj(comment)
			
			post = context.get('post')
			comment.post = post
			comment.save()
			
			return redirect(url_for('posts.detail', slug=slug))

		return render_template('posts/detail.html', **context)

class CommentDelete(MethodView):
	decorators=[login_required]
	
	def get(self,comment, slug):
		comment = Comment.get(id=int(comment))
		comment.delete_instance()
		
		return redirect(url_for('posts.detail', slug=slug))

# Register the urls
posts.add_url_rule('/', view_func=ListView.as_view('list'))
posts.add_url_rule('/index/', view_func=ListView.as_view('index'))
posts.add_url_rule('/<int:page>/', view_func=ListView.as_view('page'))
posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
posts.add_url_rule('/comment/delete/<slug>/<comment>/', view_func=CommentDelete.as_view('delete'))
