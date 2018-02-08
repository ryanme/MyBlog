#!coding:utf8
from MyServer.app.models import ArticlesInfo, Articles, User
from MyServer.app import db
import json
import requests
import bleach
import markdown
from flask_wtf import Form
from wtforms import (
    StringField,
    TextField,
    TextAreaField,
    PasswordField,
    BooleanField,
    ValidationError
)
from wtforms.validators import DataRequired, Length, EqualTo,URL


def get_articlesnums(type):
    allartielces = ArticlesInfo.query.filter_by(type=type).all()
    return len(allartielces)

def get_content(id):
    article = Articles.query.filter_by(id=id).first()
    content = article.content
    return content

def get_type(id):
    articleinfo = ArticlesInfo.query.filter_by(id=id).first()
    type = articleinfo.type
    return type

def get_bloglist(pageid, type):
    page_size = 10
    results = ArticlesInfo.query.filter(ArticlesInfo.type.like('%' + type + '%')).paginate(int(pageid), int(page_size),False)
    # 遍历时要加上items
    results_list = results.items
    bloglist = []
    for result in results_list:
        i = {
            'id': result.id,
            'title': result.title,
            'author': result.author,
            'type': result.type,
            'time': result.time,
            'visit': result.visit
        }
        bloglist.append(i)
    return bloglist

# 增加访问量
def add_visit(id):
    articleinfo = ArticlesInfo.query.filter_by(id=id).first()
    articleinfo.visit += 1
    db.session.add(articleinfo)
    db.session.commit()
    db.session.close()

# 获取实时新闻接口，调用莫网站
def get_news(time, type):
    url = 'http://www.donews.com/column/get_news_flash'
    params = {'datetime': time,
              'type': type,
              }
    response = requests.get(url, params).text
    info = json.loads(response)
    return info

# 获取缩略内容
def get_short_content(id):
    article = Articles.query.filter_by(id=1).first()
    content = article.content
    short_content = content
    return content

'''
body_html=db.Column(db.Text)
'''

#处理body字段变化的函数
@staticmethod
def on_changed_post(target,value,oldvalue,initiaor):
    allow_tags=['a','abbr','acronym','b','blockquote','code',
                'em','i','li','ol','pre','strong','ul',
                'h1','h2','h3','p','img']
    #转换markdown为html，并清洗html标签
    target.body_html=bleach.linkify(bleach.clean(
        markdown(value,output_form='html'),
        tags=allow_tags,strip=True,
        attributes={
            '*': ['class'],
            'a': ['href', 'rel'],
            'img': ['src', 'alt'],#支持<img src …>标签和属性
        }
))

class LoginForm(Form):
    """Login Form"""
    username = StringField('Username', [DataRequired(), Length(max=255)])
    passwd = PasswordField('Password', [DataRequired()])

    def validate(self):
        """Validator for check the account information."""
        check_validata = super(LoginForm, self).validate()

        # If validator no pass
        if not check_validata:
            return False

        # Check the user whether exist.
        user = User.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password.')
            return False

        # Check the password whether right.
        if not user.check_passwd(self.passwd.data):
            self.username.errors.append('Invalid username or password.')
            return False

        return True