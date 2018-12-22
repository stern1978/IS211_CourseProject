import os
import requests
from flask import Flask, render_template, request, redirect, session, g, url_for, flash
import sqlite3
from contextlib import closing

DATABASE = 'books.db'
SECRET_KEY = 'secret_key'
USERNAME = 'admin'
PASSWORD = 'password'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def get_db():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            return redirect('/library')
    return render_template('login.html', error=error)

@app.route('/library', methods = ['GET'])
def library():
    if session['logged_in'] == False:
        return redirect('/login')
    else:
        cur = g.db.execute('SELECT title, author, pages, rating, thumbnail, link, description FROM books order by title')
        books = [dict(title=row[0], author=row[1], pages=row[2], rating=row[3], thumbnail=row[4], link=row[5], description=row[6]) for row in cur.fetchall()]
        return render_template('library.html', books = books)

@app.route('/search', methods = ['GET', 'POST'])
def search():
    if session['logged_in'] == False:
        return redirect('/login')
    else:
        if request.method == 'POST':
            print ('Searching')
            find = (request.form['booksearch'])
            find = find.replace(' ', '+')
            r = requests.get(url="https://www.googleapis.com/books/v1/volumes?q=" + find)
            print r.url
            rj = r.json()

            try:
                for i in (rj['items']):
                    try:
                        title = (i['volumeInfo']['title'])
                    except Exception as e:
                        title = 'Unknown'
                    try:
                        subtitle = (i['volumeInfo']['subtitle'])
                    except Exception as e:
                        subtitle = 'Unknown'
                    try:
                        author = (i['volumeInfo']['authors'][0])
                    except Exception as e:
                        author = 'Unknown'
                    try:
                        pageCount = (i['volumeInfo']['pageCount'])
                    except Exception as e:
                        pageCount = 'Unknown'
                    try:
                        rating = (i['volumeInfo']['averageRating'])
                    except Exception as e:
                        rating = 'Unknown'
                    try:
                        thumbnail = (i['volumeInfo']['imageLinks']['thumbnail'])# + '.jpg')
                    except Exception as e:
                        thumbnail = 'Unknown'
                    try:
                        link = (i['volumeInfo']['previewLink'])
                    except Exception as e:
                        link = 'Unknown'
                    try:
                        description = (i['volumeInfo']['description'])
                        print description
                    except Exception as e:
                        description = 'Unknown'
                    g.db.execute('INSERT INTO books (title, author, pages, rating, thumbnail, link, description) VALUES (?,?,?,?,?,?,?)', [title, author, pageCount, rating, thumbnail, link, description])
                    g.db.commit()
                    return redirect('/library')

                    #return render_template('search.html', title=title, author=author, pageCount=pageCount, rating=rating)
            except:
                return redirect('/library')

@app.route('/delete', methods=['POST'])
def delete():
    if session['logged_in'] == False:
        return redirect('/login')
    else:
        print 'remove'
        b = request.form['delete']
        print b
        g.db.execute('DELETE FROM books WHERE title=?', (b,))
        #g.db.exicute(delete)
        g.db.commit()
        return redirect('/library')

if __name__ == "__main__":
    app.run(debug = True)
    connect_db()
