from flask import *
import requests
import json
from bs4 import BeautifulSoup
import sqlite3
import os

app = Flask(__name__)
app.secret_key = ('pass')


#login form
'''@app.route('/login', methods=['GET', 'POST'])
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
        return render_template('login.html', error=error)'''

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


#function to add books to account
@app.route('/search', methods=['GET','POST'])
def search():

    #variable for html form
    isbn = request.form["isbn"]

    # Scrape website
    #book_isbn = '9781449372620'
    r = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:{}".format(isbn))
    soup = BeautifulSoup(r.content, 'html.parser')
    data = json.loads(soup.text)
    try:
        title = data['items'][0]['volumeInfo']['title']
        print(title)
    except KeyError:
        print('***TITLE COULD NOT BE FOUND***')



    #path = os.path.dirname(os.path.abspath(__file__))
    #conn = sqlite3.connect(path+'/books.db')
    #c = conn.cursor()
    #c.execute("INSERT INTO books (isbn) VALUES (?)",[isbn])
    #conn.commit()

    return render_template('search.html', title=title)


if __name__=="__main__":
    app.run(debug=True)