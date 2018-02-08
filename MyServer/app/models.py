#!coding:utf8
from MyServer.app import db
from MyServer.app import bcypt

class ArticlesInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(10), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    time = db.Column(db.DateTime)
    visit = db.Column(db.Integer, default=0)

    articles_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    articles = db.relationship('Articles', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, author, type, time, visit, articles):
        self.title = title
        self.author = author
        self.type = type
        self.time = time
        self.visit = visit
        self.articles = articles

    def __repr__(self):
        return '<ArticlesInfo %r>' % self.title

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return '<Articles %r>' % self.content

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(45), primary_key=True)
    username = db.Column(db.String(255))
    passwd = db.Column(db.String(255))

    # author = db.Column(db.String, db.ForeignKey('articlesInfo.id'))
    # articles = db.relationship('ArticlesInfo', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, id, username, passwd):
        self.id = id
        self.username = username
        # 在设定密码的时候，将明文密码转换成为 Bcrypt 类型的哈希值。
        self.passwd = self.set_passwd(passwd)

    def __repr__(self):
        """Define the string format for instance of User."""
        return "<Model User `{}`>".format(self.username)

    def set_passwd(self, passwd):
        """Convert the password to cryptograph via flask-bcrypt"""
        return bcypt.generate_password_hash(passwd)

    # 检验输入的密码的哈希值，与存储在数据库中的哈希值是否一致。
    def check_passwd(self, passwd):
        return bcypt.check_password_hash(self.passwd, passwd)



