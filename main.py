from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:12345@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    body = db.Column(db.String(1500))
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.pub_date = datetime.utcnow()

#redirect route to blog page from main index page
@app.route('/')
def index():
    return redirect('/blog')

#shows all blog posts
@app.route('/blog', methods=['POST','GET'])
def blog():
    #check for query parameters
    blog_id = request.args.get('id')

    if blog_id:
        post = Blog.query.get(blog_id)
        blog_title = post.title
        blog_body = post.body

        #Case 1
        return render_template('page.html', title="Blog"+blog_id, blog_title=blog_title, blog_body=blog_body)

    #if no post selected, show all posts
    else:
        blogs = Blog.query.order_by(desc(Blog.pub_date)).all()
        return render_template('blog.html', title="Build a Blog", blogs=blogs)


@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        title_error = ''
        body_error = ''

        #error messages if entry not complete
        if blog_title == "":
            flash("Error: Please enter a title!", category='error')
            return redirect('/newpost')
        if blog_body == "":
            flash("Error: Please enter some content!", category='error')
            return redirect('/newpost')

        #if both fields are completed
        if not title_error and not body_error:
            new_blog = Blog(blog_title, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            #Case 2: redirect to new post page
            return redirect('/blog?id={0}'.format(new_blog.id))

    return render_template('post.html', title="Add a Blog")

if __name__ == '__main__':
    app.run()
