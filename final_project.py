from flask import *
import requests
import json

book_isbn = '9780545010221'
r = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:{}".format(book_isbn))
print(r.url)

app = Flask(__name__)

@app.route('/')
def hello():
    return r.json()



if __name__ == '__main__':
    app.run(debug=True)