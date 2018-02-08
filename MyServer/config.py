#!coding:utf8
import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')  #数据库文件的路径
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')  #是文件夹，我们将会把 SQLAlchemy-migrate 数据文件存储在这里
SQLALCHEMY_TRACK_MODIFICATIONS = False