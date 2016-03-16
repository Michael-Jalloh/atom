from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from flask.ext.login import login_required, current_user
from wtfpeewee.orm import model_form
from playhouse.flask_utils import get_object_or_404
from models import Post, Comment, PostIndex

admin = Blueprint('admin', __name__, template_folder='templates')


class List(MethodView):
	decorators = [login_required]

	def get(self):
		posts = current_user.posts.order_by(Post.timestamp.desc())
		return render_template('admin/list.html', posts=posts)


class Detail(MethodView):
	decorators = [login_required]

	def get_context(self, slug=None):
		form_cls = model_form(Post, exclude=('timestamp', 'comments','slug','author'))

		if slug:
			query = Post.select()
			post = get_object_or_404(query, Post.slug ==slug)
			if request.method == 'POST':
				form = form_cls(request.form, intial=post.content)
			else:
				form = form_cls(obj=post)
		else:
			post = Post()
			form = form_cls(request.form)

		context = {
			'post': post,
			'form': form,
			'create': slug is None
		}
	
		return context

	def get(self, slug):
		context = self.get_context(slug)
		return render_template('admin/detail.html', **context)

	def post(self, slug):
		context = self.get_context(slug)
		form = context.get('form')

		if form.validate():
			post = context.get('post')
			form.populate_obj(post)
			post.author = int(current_user.id)
			post.save()

			return redirect(url_for('admin.index'))
		return render_template('admin/detail.html', **context)


class Delete(MethodView):
	def get(self,slug):
		query = Post.select()
		post = get_object_or_404(query,Post.slug==slug)
		for comment in post.comments:
			comment.delete_instance()
		PostIndex.delete().where(PostIndex.post_id ==post.id).execute()
		post.delete_instance()
		return redirect('/admin/')
		


# Register the urls
admin.add_url_rule('/admin/', view_func=List.as_view('index'))
admin.add_url_rule('/admin/create/', defaults={'slug': None}, view_func=Detail.as_view('create'))
admin.add_url_rule('/admin/<slug>/', view_func=Detail.as_view('edit'))
admin.add_url_rule('/admin/delete/<slug>/', view_func=Delete.as_view('delete'))
