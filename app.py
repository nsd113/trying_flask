from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    dateposted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)


all_posts = [ #just to delite it later
    {
        'title': 'Post 1',
        'content': 'This is the content of post 1.',
        'author': 'Zilazni'
    },
    {
        'title': 'Post 2',
        'content': 'This is the content of post 2.'
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts', methods=['GET', 'POST'])

def posts():

    if request.method == 'POST': #read all data from the form and save it to DB
        post_title = request.form['title']
        post_content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author='Aaron')
        db.session.add(new_post) #adding to db
        db.session.commit()
        return redirect('/posts')
    else: # if we are getting- display existing db 
        all_posts = BlogPost.query.order_by(BlogPost.dateposted).all()

    return render_template('posts.html', posts=all_posts) 

if __name__ == "__main__":
    app.run(debug=True)