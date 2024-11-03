import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY']= "your secret key"

# Function to open a connection to the database.db file
def get_db_connection():
    # create connection to the database
    conn = sqlite3.connect('database.db')
    
    # allows us to have name-based access to columns
    # the database connection will return rows we can access like regular Python dictionaries
    conn.row_factory = sqlite3.Row

    #return the connection object
    return conn

#dunction to reterive...
def get_post(id):
    conn= get_db_connection
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()

    if post is None:
        abort(404)

        return post 


# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():
    #get a connection to the database 
    conn = get_db_connection()

    #execute a query to read all post from the post table in the database
    posts = conn.execute('SELECT * FROM posts').fetchall()

    #close the connnetion 
    conn.close()

    #send the post to the index.html template to be displayed
    return render_template("index.html", posts=posts)

    return "<h1>Welcome to My Blog</h1>"


# route to create a post
@app.route('/create/', methods=('GET', 'POST'))
def create():
    #determine if the page is being requested with a POST or GET request
    if request.method == 'POST' :
       #get the title 
        title = request.form['title']
        content = request.form['content']

       #display error messgae if title of content is not submitted
       
       #else maeke a adatabase conenct and tonsert blog post contetn
        if not title:
            flash("Title is required")
        elif not content:
            flash('Content is required')
        else:
            conn = get_db_connection()
            #insert data into database
            conn.execute('INSERT INTO posts (title,content) VALUES (?, ?)', (title,content))
            conn.commit()
            conn.close()
            return redirect(url_for("index"))    

    return render_template('create.html')

#create a route to edit post.Load page eith get or post method 
#pass
@app.route('/<int:id>/edit/', methode=('GET','POST'))
def edit(id):
    #get the post from the database
    post = get_post(id)

    #determine if the oage was requested eith get or psot
    if request.method == 'POST':
        #get the title and content
        title = request.form['title']
        content = request.form['content']

        #if not 
        if not title:
            flash('Title is required')
        elif not content:
            flash('Content is required')
        else:
            conn = get_db_connection

            conn.execute('UPDATE post SET title = ?, content =? WHERE id is =?', (title, content, id))
            conn.commit
            conn.close()

            #redirect to the home page 
            return redirect(url_for('index'))

   
    #if POST, process the form data
    return render_template('edit.html', post=post)

#create a route to delete post
# delete page with post methods
#the post id the url parametr 
@app.route('/int:id>/delete', methods=('POST',))
def delete(id):
    #get the post
    post = get_post(id)

    #connect the delte quiere
    conn = get_db_connection()

    #flash sucess mesbggae 
    conn.execute("DELETE from post WHERE id = ?", (id,))
    #got back to home page
    conn.commit()
    conn.close()

    flash ('"{}" was succesfully delted!'.format(post{'title'}))

    return redirect(url_for('index'))

app.run(port=5008)