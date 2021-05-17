from flask import Flask, request, session, render_template, redirect, url_for
import requests
import json
from bs4 import BeautifulSoup
import sqlite3
import os

app = Flask(__name__)
app.secret_key = ('pass')

#login form
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin':
            error = 'Invalid Username or Password.'
            return render_template('login.html', error=error)
        elif request.form['password'] != 'password':
            error = 'Invalid Username of Password.'
            return render_template('login.html', error=error)
        else:
            #start session
            session['logged_in'] = True
            if session.get('logged_in') != None:
                print('session started')
            return redirect('/maindisplay')
    else:
        return render_template('login.html', error=error)


# Main Display
@app.route('/maindisplay', methods=['GET'])
def books():

    #db connection
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/books.db')
    c = conn.cursor()

    # Select statements to retrieve book table data
    c.execute("SELECT * FROM books")
    books_info = c.fetchall()

    return render_template('maindisplay.html', books_info=books_info)


#function to find book information
@app.route('/search', methods=['GET','POST'])
def search():

    #variable for html form
    book_isbn = request.form['book_isbn']

    # Scrape website
    #Flask isbn = '9781449372620'
    #Harry Potter isbn ='9780545139700'
    #Awaken the Giant isbn = '1471167518'

    r = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:{}".format(book_isbn))
    soup = BeautifulSoup(r.content, 'html.parser')
    data = json.loads(soup.text)

    try:
        global title
        title = data['items'][0]['volumeInfo']['title']
    except KeyError:
        title = 'Not Found'

    try:
        author = data['items'][0]['volumeInfo']['authors'][0]
    except KeyError:
        author = 'Not Found'

    try:
        page_count = data['items'][0]['volumeInfo']['pageCount']
    except KeyError:
        page_count = 'Not Found'

    try:
        average_rating = data['items'][0]['volumeInfo']['averageRating']
    except KeyError:
        average_rating = 'Not Found'

    # Connect to DB
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/books.db')
    c = conn.cursor()

    # Select statements to retrieve book table data
    c.execute("SELECT * FROM books")
    books_info = c.fetchall()

    return render_template('maindisplay.html', title=title, author=author, page_count=page_count, average_rating=average_rating, books_info=books_info)


# Function to add books to collection
@app.route('/book_add', methods=['GET','POST'])
def book_add():
    # variable for html form
    isbn = request.form['isbn']

    r = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:{}".format(isbn))
    soup = BeautifulSoup(r.content, 'html.parser')
    data = json.loads(soup.text)

    try:
        global title
        title = data['items'][0]['volumeInfo']['title']
    except KeyError:
        title = 'Not found'

    try:
        author = data['items'][0]['volumeInfo']['authors'][0]
    except KeyError:
        author = 'Not found'

    try:
        page_count = data['items'][0]['volumeInfo']['pageCount']
    except KeyError:
        page_count = 'Not found'

    try:
        average_rating = data['items'][0]['volumeInfo']['averageRating']
    except KeyError:
        average_rating = 'Not found'

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/books.db')
    c = conn.cursor()
    #changed brackets to parantheses
    try:
        c.execute("INSERT INTO books (title, author, pages, rating, isbn) VALUES (?,?,?,?,?)",[title, author, page_count, average_rating, isbn])
    except Exception:
        flash("Title is already added",'error')
        return redirect('/maindisplay')
    conn.commit()
    return redirect('/maindisplay')


#delete record
@app.route('/delete_book', methods=['POST'])
def delete_book():
    row = request.form['row']

    # Connect to DB
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/books.db')
    c = conn.cursor()

    #delete
    c.execute("DELETE FROM books WHERE book_id=(?)",(row,))
    conn.commit()

    return redirect('/maindisplay')

if __name__=="__main__":
    app.run(debug=True)
