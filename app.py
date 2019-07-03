from flask import Flask, render_template, request, redirect, url_for
from flask_pager import Pager
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from bleach import clean
import sqlite3

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\dewijones\PycharmProjects\week4\blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PAGE_SIZE'] = 5
app.config['VISIBLE_PAGE_COUNT'] = 10

db = SQLAlchemy(app)

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        result = request.form['search-input']
        page = request.args.get('page', 1, type=int)
        per_page = 10

        # Avoiding raw SQL for fear of SQL injection
        posts = Blogpost.query.filter(Blogpost.content.contains(result)).paginate(page, per_page, error_out=False)

        return render_template('index.html', posts=posts)

    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Avoiding raw SQL for fear of SQL injection
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).paginate(page, per_page, error_out=False)

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

    # Escaping data where the following HTML characters are allowed <b>, <i> and <a>.
    title = clean(request.form['title'])
    subtitle = clean(request.form['subtitle'])
    author = clean(request.form['author'])
    content = clean(request.form['content'], tags=['b', 'i', 'a'])

    post = Blogpost(title=title, subtitle=subtitle, author=author, content= content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

####################################################################################################

@app.route('/unsafe_index', methods=['GET', 'POST'])
# @app.route('/unsafe_index/<int:page>')
def unsafe_index():
    conn = sqlite3.connect('unsafeblog.db')


    post_query = "SELECT * FROM blogpost ORDER BY date_posted DESC LIMIT 10;"
    posts = conn.execute(post_query)

    list_of_posts = []
    for post in posts:
        list_of_posts.append(post)

    if request.method == 'POST':
        result = request.form['search-input']

        # Avoiding raw SQL for fear of SQL injection
        post_query = "SELECT * FROM blogpost WHERE content LIKE '%"+ result + "%'"
        posts = conn.execute(post_query)

        list_of_posts = []
        for post in posts:
            list_of_posts.append(post)

        return render_template('unsafe_index.html', posts=list_of_posts)

    return render_template('unsafe_index.html', posts=list_of_posts)

@app.route('/unsafe_post/<string:post_id>')
def unsafe_post(post_id):
    conn = sqlite3.connect('unsafeblog.db')

    # Unsafe value
    # SQL injection possible
    post_query = "SELECT * FROM blogpost WHERE id = "+ post_id +""
    print(post_query)
    cursor = conn.cursor()
    post = cursor.execute(post_query)
    row = post.fetchone()
    return render_template('unsafe_post.html', post=row)

@app.route('/unsafe_add')
def unsafe_add():
    return render_template('unsafe_add.html')

@app.route('/unsafe_addpost', methods=['POST'])
def unsafe_addpost():
    conn = sqlite3.connect('unsafeblog.db')

    # SQL injection INSERT in content place asd'); DROP TABLE users --' )
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post_query = "INSERT INTO blogpost (title, subtitle, author, date_posted, content) VALUES('"+ title +"','"+ subtitle +"', '"+ author +"' , '"+ datetime.now().strftime("%Y-%m-%d %H:%M:%S") +"', '"+ content +"' )"
    print(post_query)
    conn.executescript(post_query)
    conn.commit()

    return redirect(url_for('unsafe_index'))

if __name__ == '__main__':
    app.run(debug=True)