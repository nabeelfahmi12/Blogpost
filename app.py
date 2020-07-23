from flask import Flask , render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Data.db'
db = SQLAlchemy(app)

class BlogPost(db.Model) :
    id = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(100) , nullable=False)
    content = db.Column(db.Text , nullable=False)
    author = db.Column(db.String(20) , nullable=False , default='Owner of APP')
    date_posted = db.Column(db.DateTime , nullable=False , default=datetime.utcnow)

    def __repr__(self) :
        return 'Blog post' + str(self.id)


@app.route('/')
def home_page() :
    return render_template('index.html')

@app.route("/posts/new" , methods=["Get","Post"])
def newposts() :
    if request.method == "POST" :
        post_title = request.form["title"]
        post_content = request.form["content"]
        post_author = request.form["author"]
        new_post = BlogPost(title= post_title , content= post_content , author= post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect("/posts")
    else :
        return render_template("new_post.html" )


@app.route('/posts')
def posts() :
    all_post = BlogPost.query.order_by(BlogPost.date_posted).all()
    return render_template("posts.html" , posts=all_post)

@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods= ['GET','POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form["content"]
        post.author = request.form["author"]
        db.session.commit()
        return redirect('/post')
    else :
        return render_template('edit.html', post = post)

@app.route("/home/user/<string:name>/posts/<int:id>")
def hello_world(name , id) :
    return "Hello," + name + ",Your id is: " + str(id)


@app.route("/onlyget" , methods=({'GET' , 'POST'}))
def get_req() :
    return 'you can only get this web page'


if __name__ == '__main__' :
    app.run(debug=False)
