from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\dewijones\PycharmProjects\week4\blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).paginate(page, per_page, error_out=False)

    return render_template('index.html', posts=posts)

@app.route('/', methods=['GET', 'POST'])
def search():
    result = request.form['search-input']

    page = request.args.get('page', 1, type=int)
    per_page = 10
    posts = Blogpost.query.filter(Blogpost.content.contains(result)).paginate(page, per_page, error_out=False)

    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()

    return render_template('post.html', post=post)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)