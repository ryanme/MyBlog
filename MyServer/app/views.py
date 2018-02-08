#!coding:utf8
from flask import render_template, request, jsonify, Markup, url_for, Response, abort, redirect, flash
from flask_login import login_required, LoginManager, login_user
from MyServer.app import app
from MyServer.app.forms import *
from MyServer.app import ticketprice
import os
from datetime import datetime
from uuid import uuid4
from MyServer.app.models import User,ArticlesInfo,Articles


@app.route('/', methods=['GET'])
def index():
    # user = User(id=str(uuid4()), username='ryan', passwd='wsdsl19930519!@#')
    # db.session.add(user)
    # db.session.commit()
    # user = User.query.filter_by(username='ryan').first()
    # print(user.passwd)
    return render_template('blog.html', title="Linux")

@app.route('/blog/linux/', methods=['GET'])
def linux():
    return render_template('blog.html', title="Linux")

@app.route('/blog/test/', methods=['GET'])
def blog():
    return render_template('blog.html', title="测试")

@app.route('/blog/sql/', methods=['GET'])
def sql():
    return render_template('blog.html', title="数据库")

@app.route('/blog/python/', methods=['GET'])
def python():
    return render_template('blog.html', title="Python")

@app.route('/live/', methods=['GET'])
def live():
    return render_template('live.html', title="慢生活")

@app.route('/about_me/', methods=['GET'])
def about_me():
    return render_template('about.html', title="关于我")

@app.route('/share/music/', methods=['GET'])
def music():
    return render_template('music.html', title="音乐-分享")

@app.route('/share/movie/', methods=['GET'])
def movie():
    return render_template('movie.html', title="电影-分享")

@app.route('/share/website/', methods=['GET'])
def website():
    return render_template('website.html', title="站点-分享")

@app.route('/article/<int:id>/')
def article(id):
    content = get_content(id)
    type=get_type(id)
    html = Markup(content)# 转义
    add_visit(id) # 访问量+1
    return render_template('article.html', article_content=html, title=type)

# 根据页码获取文章信息接口
@app.route('/api/articles')
def get_articles():
    type = request.args.get('type')
    pageid = request.args.get('pageid')
    # bloglist = common.get_bloglist(pageid, type)
    bloglist = get_bloglist(pageid, type)
    result = {}
    nums = get_articlesnums(type)
    result['data']  = {}
    result['data']['bloglist']= bloglist
    result['data']['total'] = nums
    result['msg'] = '成功'
    result['status'] = 0
    return jsonify(result)

# 获取新闻
@app.route('/api/news')
def get_fresh_news():
    time = request.args.get('datetime')
    type = request.args.get('type')
    result = get_news(time, type)
    return jsonify(result)

@app.route('/markdown/')
# @login_required
def markdown():
    return render_template('markdown.html')

@app.route('/markdown2/')
def markdown2():
    return render_template('markdown2.html')

@app.route('/putcontent')
def put_content():
    pass

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'), 404

@app.route('/login')
@app.route('/login/')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user()
        flash('Logged in successfully.')

        next = request.args.get('next')
        if not next_is_valid(next):
            return abort(400)

        return redirect(next or url_for('index'))
    return render_template('login.html', form=form)

@app.route('/layui')
def layui():
    return render_template('layui.html')

@app.route('/ticket', methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        return render_template('tickets.html',
                       title='票价')
    elif request.method == 'POST':
        startlocation = request.args.get('startlocation')
        endlocation = request.args.get('endlocation')
        time = request.args.get('time')
        response = "起点:" + str(startlocation) + "终点:" + str(endlocation) + "日期:" + time
        map1 = "<h1>请求成功</h1>"
        return map1


@app.route('/ticketinfo')
def ticketinfo():
    from_station = request.args.get('from_station')
    to_station = request.args.get('to_station')
    time = request.args.get('time')
    data = ticketprice.get_price(from_station, to_station, time)
    res = {
        "code": 0,
        "msg": "",
        "count": 1000,
        "data": data
    }
    return jsonify(res)

@app.route('/user/')
def userinfo():
    res={"code":0,"msg":"","count":1000,"data":[{"id":10000,"username":"user-0","sex":"女","city":"城市-0","sign":"签名-0","experience":255,"logins":24,"wealth":82830700,"classify":"作家","score":57},{"id":10001,"username":"user-1","sex":"男","city":"城市-1","sign":"签名-1","experience":884,"logins":58,"wealth":64928690,"classify":"词人","score":27},{"id":10002,"username":"user-2","sex":"女","city":"城市-2","sign":"签名-2","experience":650,"logins":77,"wealth":6298078,"classify":"酱油","score":31},{"id":10003,"username":"user-3","sex":"女","city":"城市-3","sign":"签名-3","experience":362,"logins":157,"wealth":37117017,"classify":"诗人","score":68},{"id":10004,"username":"user-4","sex":"男","city":"城市-4","sign":"签名-4","experience":807,"logins":51,"wealth":76263262,"classify":"作家","score":6},{"id":10005,"username":"user-5","sex":"女","city":"城市-5","sign":"签名-5","experience":173,"logins":68,"wealth":60344147,"classify":"作家","score":87},{"id":10006,"username":"user-6","sex":"女","city":"城市-6","sign":"签名-6","experience":982,"logins":37,"wealth":57768166,"classify":"作家","score":34},{"id":10007,"username":"user-7","sex":"男","city":"城市-7","sign":"签名-7","experience":727,"logins":150,"wealth":82030578,"classify":"作家","score":28},{"id":10008,"username":"user-8","sex":"男","city":"城市-8","sign":"签名-8","experience":951,"logins":133,"wealth":16503371,"classify":"词人","score":14},{"id":10009,"username":"user-9","sex":"女","city":"城市-9","sign":"签名-9","experience":484,"logins":25,"wealth":86801934,"classify":"词人","score":75}]}
    return jsonify(res)

# 图片上传处理
@app.route('/upload/', methods=['POST'])
def upload():
    file=request.files.get('editormd-image-file')
    if not file:
        res={
            'success':0,
            'message':u'图片格式异常'
        }
    else:
        ex=os.path.splitext(file.filename)[1]
        filename=datetime.now().strftime('%Y%m%d%H%M%S')+ex
        file.save(os.path.join(app.config['SAVEPIC'],filename))
        #返回
        res={
            'success':1,
            'message':u'图片上传成功',
            'url':url_for('.image',name=filename)
        }
    return jsonify(res)

#编辑器上传图片处理
@app.route('/image/<name>')
def image(name):
    with open(os.path.join(app.config['SAVEPIC'],name),'rb') as f:
        resp=Response(f.read(),mimetype="image/jpeg")
    return resp