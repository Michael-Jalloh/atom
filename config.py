import os

APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = 'sqliteext:///%s' % os.path.join(APP_DIR, 'blog.db')
DEBUG = True
SECRET_KEY = os.urandom(24) # Used bt Flask to encrypt session cokkie.
SITE_WIDTH = 800
POST_PER_PAGE = 5

