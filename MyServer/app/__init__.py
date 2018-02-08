from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__, static_url_path='', root_path='/Users/ryan/Documents/Python Project/MyServer')
app.config.from_object('config')
db = SQLAlchemy(app)
db.init_app(app)
bcypt = Bcrypt()
bcypt.init_app(app)
#注册监听事件
# db.event.listen(Posts.body, 'set', Posts.on_changed_post)
from MyServer.app import views
