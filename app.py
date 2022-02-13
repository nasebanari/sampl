from flask import Flask
from flask import render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    tag = db.Column(db.String(12), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(pytz.timezone('Asia/Tokyo')))


@app.route("/",methods=['GET','POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.all()
    return render_template('index.html',posts=posts)

@app.route("/create.html",methods=['GET','POST'])
def create():
    if request.method == 'POST':
       title = request.form.get('title')
       tag = request.form.get('tag')
       body = request.form.get('body')
       post = Post(title=title,tag=tag,body=body)

       db.session.add(post)
       db.session.commit()
       return redirect('/')
    else:
       return render_template('create.html') 

@app.route('/<int:id>/update.html', methods=['GET', 'POST'])
def update(id):
   post = Post.query.get(id)
   if request.method == 'GET':
        return render_template('update.html', post=post)
   else:
       post.title = request.form.get('title')
       post.tag = request.form.get('tag')
       post.body = request.form.get('body')

       db.session.commit()
       return redirect('/')

@app.route('/<int:id>/delete', methods=['GET'])
def delete(id):
 post = Post.query.get(id)
   
 db.session.delete(post)
 db.session.commit()
 return redirect('/')

@app.route('/<int:id>/show.html', methods=['GET'])
def show(id):
   post = Post.query.get(id)
   return render_template('show.html', post=post)